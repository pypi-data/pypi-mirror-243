import torch
from torch import nn
import sys
from galvatron.core import get_args
from galvatron.core.tensor_parallel import ParallelMLP, ParallelAttention
from galvatron.core.tensor_parallel import AttnMaskType, AttnType, init_method_normal, scaled_init_method_normal

def overwrite_vision_configs(args, config):
    args.hidden_size = config.vision_config.hidden_size
    args.ffn_hidden_size = config.vision_config.intermediate_size
    args.num_layers = config.vision_config.num_hidden_layers
    args.num_attention_heads = config.vision_config.num_attention_heads
    args.max_position_embeddings = (config.vision_config.image_size // config.vision_config.patch_size) ** 2 + 1
    args.kv_channels = args.hidden_size // args.num_attention_heads
    args.attention_dropout = config.vision_config.attention_dropout
    args.dropout_prob = config.vision_config.dropout
    args.hidden_dropout = config.vision_config.dropout
    
def overwrite_text_configs(args, config):
    args.hidden_size = config.text_config.hidden_size
    args.ffn_hidden_size = config.text_config.intermediate_size
    args.num_layers = config.text_config.num_hidden_layers
    args.num_attention_heads = config.text_config.num_attention_heads
    args.max_position_embeddings = config.text_config.max_position_embeddings
    args.kv_channels = args.hidden_size // args.num_attention_heads
    args.attention_dropout = config.text_config.attention_dropout
    args.dropout_prob = config.text_config.dropout
    args.hidden_dropout = config.text_config.dropout

class CLIPAttention_tp(nn.Module):
    def __init__(self, config, modal_type = 'vision', tp_group = None):
        super().__init__()
        args=get_args()
        init_method = init_method_normal(args.init_method_std)
        scaled_init_method = scaled_init_method_normal(args.init_method_std, args.num_layers)
        self.tp_group = tp_group.group if tp_group is not None else None
        attn_mask_type = AttnMaskType.padding if modal_type == 'vision' else AttnMaskType.causal
        self.attention = ParallelAttention(init_method, 
                                        scaled_init_method, 
                                        attention_type=AttnType.self_attn,
                                        attn_mask_type=attn_mask_type,
                                        tp_group = self.tp_group)

    def forward(self, hidden_states, attention_mask, causal_attention_mask=None, output_attentions=False):
        hidden_states = hidden_states.permute(1, 0, 2)
        hidden_states, bias = self.attention(hidden_states, attention_mask)
        hidden_states = hidden_states + bias
        hidden_states = hidden_states.permute(1, 0, 2)
        return hidden_states, None

class CLIPMLP_tp(nn.Module):
    def __init__(self, config, tp_group = None):
        super().__init__()
        args=get_args()
        init_method = init_method_normal(args.init_method_std)
        scaled_init_method = scaled_init_method_normal(args.init_method_std, args.num_layers)
        self.tp_group = tp_group.group if tp_group is not None else None
        self.mlp = ParallelMLP(init_method, scaled_init_method, tp_group = self.tp_group)

    def forward(self, hidden_states):
        hidden_states, bias = self.mlp(hidden_states)
        return hidden_states + bias
    
def construct_tensor_parallel_model(model, config, tp_groups_enc):
    args = get_args()
    from CLIPModel_tensor_parallel import CLIPAttention_tp, CLIPMLP_tp, overwrite_vision_configs, overwrite_text_configs
    overwrite_vision_configs(args, config)
    for i in range(config.vision_config.num_hidden_layers):
        layer = model.vision_model.encoder.layers[i]
        setattr(layer, 'self_attn', CLIPAttention_tp(config, 'vision', tp_group = tp_groups_enc[i]))
        setattr(layer, 'mlp', CLIPMLP_tp(config, tp_group = tp_groups_enc[i]))
    overwrite_text_configs(args, config)
    for i in range(config.text_config.num_hidden_layers):
        layer = model.text_model.encoder.layers[i]
        idx = i+config.vision_config.num_hidden_layers
        setattr(layer, 'self_attn', CLIPAttention_tp(config, 'text', tp_group = tp_groups_enc[idx]))
        setattr(layer, 'mlp', CLIPMLP_tp(config, tp_group = tp_groups_enc[idx]))
    return model