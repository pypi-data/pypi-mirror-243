import os
import torch
from galvatron.utils import dict_join_dirname

# ============= HuggingFace Model Config Paths =============
def chatglm2_hf_configs(model_type):
    return os.path.join(os.path.dirname(__file__), model_type)

# ============= Set Model Config and Arguments =============
def set_model_config(config, args, overwrite_args=True):
    # ======= Arguments --> Model Config ======
    # Overwrite all model configs by manually set arguments
    if args.set_model_config_manually:
        config.padded_vocab_size=args.vocab_size
        config.hidden_size=args.hidden_size
        config.num_layers=args.num_hidden_layers
        config.num_attention_heads=args.num_attention_heads
        config.ffn_hidden_size=args.ffn_hidden_size
        config.seq_length=args.seq_length
        config.attention_dropout=args.dropout_prob
        config.hidden_dropout=args.dropout_prob
        config.kv_channels=args.hidden_size // args.num_attention_heads
        config.multi_query_attention=args.multi_query_attention
        config.torch_dtype = {"fp32": torch.float32, "fp16": torch.float16, "bf16": torch.bfloat16}[args.mixed_precision]
    # Overwrite layer number only
    elif args.set_layernum_manually:
        config.num_layers=args.num_hidden_layers
    
    # ======= Model Config --> Arguments ======
    # This step is necessary that maintains the consistency of model config and arguments.
    # Overwrite the model arguments with the model config
    overwrite_model_args(config, args)
    
    if overwrite_args: # Overwrite necessary Megatron-LM arguments with the model config
        overwrite_megatron_args(config, args)
    return config

def overwrite_megatron_args(config, args):
    args.num_layers = config.num_layers
    args.ffn_hidden_size = config.ffn_hidden_size
    args.max_position_embeddings = config.seq_length
    args.attention_dropout = config.attention_dropout
    args.hidden_dropout = config.hidden_dropout
    args.kv_channels = config.kv_channels
    args.add_bias_linear = config.add_bias_linear
    args.apply_query_key_layer_scaling = config.apply_query_key_layer_scaling
    args.attention_softmax_in_fp32 = config.attention_softmax_in_fp32
    args.use_cpu_initialization = True

# Need to overwrite the arguments with the model config
def overwrite_model_args(config, args):
    args.hidden_size = config.hidden_size
    args.ffn_hidden_size = config.ffn_hidden_size
    args.num_hidden_layers = config.num_layers
    args.num_attention_heads = config.num_attention_heads
    args.seq_length = config.seq_length
    args.vocab_size = config.padded_vocab_size
    args.multi_query_attention = 1 if config.multi_query_attention else 0

# ============= Get Model Name and Layer Configs =============
def model_name(config, args=None):
    return 'hidden%d_head%d_seqlen%d'%(config.hidden_size, config.num_attention_heads, config.seq_length)

def model_layer_configs(config):
    return [
        {'hidden_size': config.hidden_size,
         'seq_len': config.seq_length,
         'layer_num': config.num_layers
         }
    ]