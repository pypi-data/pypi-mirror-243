import torch
from torch import nn
from galvatron.core import get_args
from galvatron.core.tensor_parallel import ParallelMLP, ParallelAttention
from galvatron.core.tensor_parallel import AttnMaskType, AttnType, init_method_normal, scaled_init_method_normal

class T5LayerNorm(nn.Module):
    def __init__(self, hidden_size, eps=1e-6):
        """
        Construct a layernorm module in the T5 style No bias and no subtraction of mean.
        """
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps

    def forward(self, hidden_states):
        # layer norm should always be calculated in float32
        variance = hidden_states.to(torch.float32).pow(2).mean(-1, keepdim=True)
        hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)

        # convert into half-precision if necessary
        if self.weight.dtype in [torch.float16, torch.bfloat16]:
            hidden_states = hidden_states.to(self.weight.dtype)

        return self.weight * hidden_states

class T5LayerFF_tp(nn.Module):
    def __init__(self, config, tp_group = None):
        super().__init__()
        args=get_args()
        init_method = init_method_normal(args.init_method_std)
        scaled_init_method = scaled_init_method_normal(args.init_method_std, args.num_layers)
        self.tp_group = tp_group.group if tp_group is not None else None
        if config.feed_forward_proj == "relu":
            self.DenseReluDense = ParallelMLP(init_method, scaled_init_method, act_func='relu', tp_group=self.tp_group)
        elif config.feed_forward_proj == "gated-gelu":
            self.DenseReluDense = ParallelMLP(init_method, scaled_init_method, act_func='gelu', tp_group=self.tp_group)

        self.layer_norm = T5LayerNorm(config.d_model, eps=config.layer_norm_epsilon)
        self.dropout = nn.Dropout(config.dropout_rate)

    def forward(self, hidden_states):
        forwarded_states = self.layer_norm(hidden_states)
        forwarded_states, _ = self.DenseReluDense(forwarded_states)
        hidden_states = hidden_states + self.dropout(forwarded_states)
        return hidden_states


class T5Attention_tp(nn.Module):
    def __init__(self, config, has_relative_attention_bias=False, tp_group = None):
        super().__init__()
        self.is_decoder = config.is_decoder
        self.has_relative_attention_bias = has_relative_attention_bias

        args=get_args()
        init_method = init_method_normal(args.init_method_std)
        scaled_init_method = scaled_init_method_normal(args.init_method_std, args.num_layers)
        self.tp_group = tp_group.group if tp_group is not None else None
        if self.is_decoder:
            self.attention = ParallelAttention(
                init_method, 
                scaled_init_method, 
                attention_type=AttnType.cross_attn,
                attn_mask_type=AttnMaskType.causal,
                tp_group=self.tp_group
            )
        else:
            self.attention = ParallelAttention(
                init_method, 
                scaled_init_method, 
                attention_type=AttnType.self_attn,
                attn_mask_type=AttnMaskType.padding,
                tp_group=self.tp_group
            )

    def forward(
        self,
        hidden_states,
        mask=None,
        key_value_states=None,
        position_bias=None,
        past_key_value=None,
        layer_head_mask=None,
        query_length=None,
        use_cache=False,
        output_attentions=False,
    ):
        if self.is_decoder:
            assert(key_value_states is not None)
            attention_output, _ = self.attention(
                hidden_states,
                mask,
                encoder_output=key_value_states,
            )
        else:
            attention_output, _ = self.attention(
                hidden_states,
                mask,
            )
        outputs = (attention_output,None,None)
        return outputs


class T5Block_tp(nn.Module):
    def __init__(self, t5_block):
        super().__init__()
        self.t5_block = t5_block

    def forward(
        self,
        hidden_states,
        attention_mask=None,
        position_bias=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
        encoder_decoder_position_bias=None,
        layer_head_mask=None,
        cross_attn_layer_head_mask=None,
        past_key_value=None,
        use_cache=False,
        output_attentions=False,
        return_dict=True,
    ):
        hidden_states = hidden_states.permute(1,0,2)
        if encoder_hidden_states is not None:
            encoder_hidden_states = encoder_hidden_states.permute(1,0,2)
        layer_outputs = self.t5_block(
            hidden_states,
            attention_mask=attention_mask,
            position_bias=position_bias,
            encoder_hidden_states=encoder_hidden_states,
            encoder_attention_mask=encoder_attention_mask,
            encoder_decoder_position_bias=encoder_decoder_position_bias,
            layer_head_mask=layer_head_mask,
            cross_attn_layer_head_mask=cross_attn_layer_head_mask,
            past_key_value=past_key_value,
            use_cache=use_cache,
            output_attentions=output_attentions,
        )

        outputs = (layer_outputs[0].permute(1,0,2),) + layer_outputs[1:]
        return outputs
    
def construct_tensor_parallel_model(model, config, tp_groups_enc):
    self_config = model.encoder.config
    for i in range(config.num_layers):
        layer = model.encoder.block[i].layer
        setattr(layer[0], 'SelfAttention', T5Attention_tp(self_config, tp_group=tp_groups_enc[i]))
        layer[-1] = T5LayerFF_tp(self_config, tp_group=tp_groups_enc[i])
        setattr(model.encoder.block[i], 'layer', layer)
        model.encoder.block[i] = T5Block_tp(model.encoder.block[i])
    
    cross_config = model.decoder.config
    for i in range(config.num_decoder_layers):
        layer = model.decoder.block[i].layer
        setattr(layer[0], 'SelfAttention', T5Attention_tp(self_config, tp_group=tp_groups_enc[i+config.num_layers]))
        setattr(layer[1], 'EncDecAttention', T5Attention_tp(cross_config, tp_group=tp_groups_enc[i+config.num_layers]))
        layer[-1] = T5LayerFF_tp(cross_config, tp_group=tp_groups_enc[i+config.num_layers])
        setattr(model.decoder.block[i], 'layer', layer)
        model.decoder.block[i] = T5Block_tp(model.decoder.block[i])
    
    return model