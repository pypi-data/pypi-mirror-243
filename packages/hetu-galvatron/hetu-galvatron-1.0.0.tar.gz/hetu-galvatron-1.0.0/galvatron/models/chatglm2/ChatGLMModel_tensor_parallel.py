import torch
from torch import nn
from galvatron.core import get_args
from galvatron.core.tensor_parallel import ParallelMLP, ParallelAttention, ColumnParallelLinear
from galvatron.core.tensor_parallel import AttnMaskType, AttnType, init_method_normal, scaled_init_method_normal

try:
    from einops import rearrange
except ImportError:
    rearrange = None


def _args_to_kwargs():
    args = get_args()

    common_kwargs = {
        "params_dtype": args.params_dtype,
        "use_cpu_initialization": args.use_cpu_initialization,
        "perform_initialization": args.perform_initialization,
        "gradient_accumulation_fusion": args.gradient_accumulation_fusion,
        "sequence_parallel_enabled": args.sequence_parallel,
    }
    return common_kwargs


@torch.jit.script
def apply_rotary_pos_emb(x: torch.Tensor, rope_cache: torch.Tensor) -> torch.Tensor:
    # x: [sq, b, np, hn]
    sq, b, np, hn = x.size(0), x.size(1), x.size(2), x.size(3)
    rot_dim = rope_cache.shape[-2] * 2
    x, x_pass = x[..., :rot_dim], x[..., rot_dim:]
    # truncate to support variable sizes
    rope_cache = rope_cache[:sq]
    xshaped = x.reshape(sq, -1, np, rot_dim // 2, 2)
    rope_cache = rope_cache.view(sq, -1, 1, xshaped.size(3), 2)
    x_out2 = torch.stack(
        [
            xshaped[..., 0] * rope_cache[..., 0] - xshaped[..., 1] * rope_cache[..., 1],
            xshaped[..., 1] * rope_cache[..., 0] + xshaped[..., 0] * rope_cache[..., 1],
        ],
        -1,
    )
    x_out2 = x_out2.flatten(3)
    return torch.cat((x_out2, x_pass), dim=-1)


class ChatGLMSelfAttention_tp(nn.Module):
    def __init__(self, config, tp_group=None):
        super().__init__()
        args=get_args()
        init_method = init_method_normal(args.init_method_std)
        scaled_init_method = scaled_init_method_normal(args.init_method_std, args.num_layers)
        self.tp_group = tp_group.group if tp_group is not None else None
        self.config = config

        self.attention = ParallelAttention(init_method,
                                        scaled_init_method,
                                        attention_type=AttnType.self_attn,
                                        attn_mask_type=AttnMaskType.causal, # GLM attn mask is non-causal + causal
                                        tp_group=self.tp_group)
        
        self.projection_size = config.kv_channels * config.num_attention_heads
        self.multi_query_attention = config.multi_query_attention
        self.qkv_hidden_size = 3 * self.projection_size
        if self.multi_query_attention:
            self.num_multi_query_groups_per_partition = config.multi_query_group_num
            self.qkv_hidden_size = (
                    self.projection_size + 2 * self.attention.hidden_size_per_attention_head * config.multi_query_group_num
            )

        self.attention.query_key_value = ColumnParallelLinear(
                args.hidden_size,
                self.qkv_hidden_size,
                bias=config.add_bias_linear or config.add_qkv_bias,
                gather_output=False,
                init_method=init_method,
                async_tensor_model_parallel_allreduce=args.async_tensor_model_parallel_allreduce,
                tp_group=self.tp_group,
                **_args_to_kwargs())
        
        assert tp_group.size == 1 or config.multi_query_attention == False, ('Multi query attention currently not supports tensor parallel')
    
    def forward(self, hidden_states, attention_mask, rotary_pos_emb,  kv_cache=None, use_cache=False):
        """
        hidden_states: [seq_len, batch, hidden_size]
        attention_mask: [(1, 1), seq_len, seq_len]
        """

        # Attention heads [sq, b, h] --> [sq, b, (np * 3 * hn)]
        mixed_x_layer, _ = self.attention.query_key_value(hidden_states) # zsh comment: Megatron impl has no bias but ChatGLM impl has

        if self.multi_query_attention:
            (query_layer, key_layer, value_layer) = mixed_x_layer.split(
                [
                    self.attention.num_attention_heads_per_partition * self.attention.hidden_size_per_attention_head,
                    self.num_multi_query_groups_per_partition * self.attention.hidden_size_per_attention_head,
                    self.num_multi_query_groups_per_partition * self.attention.hidden_size_per_attention_head,
                ],
                dim=-1,
            )
            query_layer = query_layer.view(
                query_layer.size()[:-1] + (self.attention.num_attention_heads_per_partition, self.attention.hidden_size_per_attention_head)
            )
            key_layer = key_layer.view(
                key_layer.size()[:-1] + (self.num_multi_query_groups_per_partition, self.attention.hidden_size_per_attention_head)
            )
            value_layer = value_layer.view(
                value_layer.size()[:-1]
                + (self.num_multi_query_groups_per_partition, self.attention.hidden_size_per_attention_head)
            )
        else:
            new_tensor_shape = mixed_x_layer.size()[:-1] + \
                               (self.attention.num_attention_heads_per_partition,
                                3 * self.attention.hidden_size_per_attention_head)
            mixed_x_layer = mixed_x_layer.view(*new_tensor_shape)

            # [sq, b, np, 3 * hn] --> 3 [sq, b, np, hn]
            (query_layer, key_layer, value_layer) = megatron_tp.split_tensor_along_last_dim(mixed_x_layer, 3)

        # apply relative positional encoding (rotary embedding)
        if rotary_pos_emb is not None:
            query_layer = apply_rotary_pos_emb(query_layer, rotary_pos_emb)
            key_layer = apply_rotary_pos_emb(key_layer, rotary_pos_emb)

        # adjust key and value for inference
        if kv_cache is not None:
            cache_k, cache_v = kv_cache
            key_layer = torch.cat((cache_k, key_layer), dim=0)
            value_layer = torch.cat((cache_v, value_layer), dim=0)
        if use_cache:
            kv_cache = (key_layer, value_layer)
        else:
            kv_cache = None

        if self.multi_query_attention:
            key_layer = key_layer.unsqueeze(-2)
            key_layer = key_layer.expand(
                -1, -1, -1, self.attention.num_attention_heads_per_partition // self.num_multi_query_groups_per_partition, -1
            )
            key_layer = key_layer.contiguous().view(
                key_layer.size()[:2] + (self.attention.num_attention_heads_per_partition, self.attention.hidden_size_per_attention_head)
            )
            value_layer = value_layer.unsqueeze(-2)
            value_layer = value_layer.expand(
                -1, -1, -1, self.attention.num_attention_heads_per_partition // self.num_multi_query_groups_per_partition, -1
            )
            value_layer = value_layer.contiguous().view(
                value_layer.size()[:2] + (self.attention.num_attention_heads_per_partition, self.attention.hidden_size_per_attention_head)
            )
        
        # # ==================================
        # core attention computation
        # ==================================

        # implementation in ChatGLM2-6B huggingface repo
        # context_layer = self.core_attention(query_layer, key_layer, value_layer, attention_mask)

        # implementation in megatron
        if not self.attention.use_flash_attn:
            if self.attention.checkpoint_core_attention:
                context_layer = self.attention._checkpointed_attention_forward(
                    query_layer, key_layer, value_layer, attention_mask)
            else:
                context_layer = self.attention.core_attention(
                    query_layer, key_layer, value_layer, attention_mask)
        else:
            q, k, v = [rearrange(x, 's b ... -> b s ...').contiguous()
                       for x in (query_layer, key_layer, value_layer)]
            if not self.attention.sequence_parallel:
                with megatron_tp.get_cuda_rng_tracker().fork():
                    context_layer = self.attention.core_attention_flash(q, k, v)
            else:
                context_layer = self.attention.core_attention_flash(q, k, v)
            context_layer = rearrange(context_layer, 'b s h d -> s b (h d)').contiguous()
        

        output, _ = self.attention.dense(context_layer)

        return output, kv_cache


class ChatGLMMLP_tp(nn.Module):
    def __init__(self, config, tp_group=None):
        super().__init__()
        args = get_args()
        init_method = init_method_normal(args.init_method_std)
        scaled_init_method = scaled_init_method_normal(args.init_method_std, args.num_layers)
        self.tp_group = tp_group.group if tp_group is not None else None
        
        args.swiglu = True
        self.mlp = ParallelMLP(init_method, scaled_init_method, tp_group=self.tp_group)

    def forward(self, hidden_states):
        hidden_states, _ = self.mlp(hidden_states)
        return hidden_states


class GLMBlock_tp(nn.Module):
    def __init__(self, config, glm_block):
        super().__init__()
        self.config = config
        self.glm_block = glm_block
    
    def forward(self, hidden_states, attention_mask, rotary_pos_emb, kv_cache=None, use_cache=False):
        hidden_states = hidden_states.permute(1, 0, 2)
        rotary_pos_emb = rotary_pos_emb.permute(1, 0, 2, 3)
        outputs = self.glm_block(hidden_states, attention_mask, rotary_pos_emb, kv_cache=kv_cache, use_cache=use_cache)
        output = outputs[0].permute(1, 0, 2)
        return output
    
def construct_tensor_parallel_model(model, config, tp_groups_enc):
    for i in range(config.num_layers):
        layer = model.transformer.encoder.layers[i]
        setattr(layer, 'self_attention', ChatGLMSelfAttention_tp(config, tp_group=tp_groups_enc[i]))
        setattr(layer, 'mlp', ChatGLMMLP_tp(config, tp_group=tp_groups_enc[i]))
        model.transformer.encoder.layers[i] = GLMBlock_tp(config, layer)
    return model