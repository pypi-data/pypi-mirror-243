import os
from galvatron.utils import dict_join_dirname

# ============= HuggingFace Model Config Paths =============
path_dict =  {
    't5-base': 't5-base.json',
    't5-large': 't5-large.json'
}

def t5_hf_configs(model_type):
    global path_dict
    path_dict = dict_join_dirname(path_dict, os.path.dirname(__file__))
    return path_dict[model_type]

# ============= Set Model Config and Arguments =============
def set_model_config(config, args, overwrite_args=True):
    # ======= Arguments --> Model Config ======
    # Overwrite all model configs by manually set arguments
    if args.set_model_config_manually:
        config.vocab_size=args.vocab_size
        config.d_model=args.hidden_size
        config.num_layers=args.num_encoder_layers
        config.num_decoder_layers=args.num_decoder_layers
        config.num_heads=args.num_attention_heads
        config.d_ff=args.hidden_size*4
        config.n_positions=args.seq_length
        config.dropout_rate=args.dropout_prob
    # Overwrite layer number only
    elif args.set_layernum_manually:
        config.num_layers=args.num_encoder_layers
        config.num_decoder_layers=args.num_decoder_layers
    
    # ======= Model Config --> Arguments ======
    # This step is necessary that maintains the consistency of model config and arguments.
    # Overwrite the model arguments with the model config
    overwrite_model_args(config, args)
    
    if overwrite_args: # Overwrite necessary Megatron-LM arguments with the model config
        overwrite_megatron_args(config, args)
    return config

def overwrite_megatron_args(config, args):
    args.hidden_size = config.d_model
    args.num_layers = config.num_layers + config.num_decoder_layers
    args.num_attention_heads = config.num_heads
    args.ffn_hidden_size = config.d_ff
    args.max_position_embeddings = config.n_positions
    args.attention_dropout = config.dropout_rate
    args.hidden_dropout = config.dropout_rate
    args.use_cpu_initialization = True

# Need to overwrite the arguments with the model config
def overwrite_model_args(config, args):
    args.hidden_size = config.d_model
    args.num_encoder_layers = config.num_layers
    args.num_decoder_layers = config.num_decoder_layers
    args.num_attention_heads = config.num_heads
    args.seq_length = config.n_positions
    args.vocab_size = config.vocab_size

# ============= Get Model Name and Layer Configs =============
def model_name(config, args=None):
    return 'hidden%d_head%d_seqlen%d'%(config.d_model, config.num_heads, config.n_positions)

def model_layer_configs(config):
    return [
        {
            'hidden_size': config.d_model,
            'seq_len': config.n_positions,
            'layer_num': config.num_layers
        },
        {
            'hidden_size': config.hidden_size,
            'seq_len': config.n_positions,
            'layer_num': config.num_decoder_layers
        }
    ]