import os
from galvatron.utils import dict_join_dirname

# ============= HuggingFace Model Config Paths =============
path_dict =  {
    'swin-huge-32': 'swin-huge-layer32-patch4-window7-224.json',
    'swin-huge-48': 'swin-huge-layer48-patch4-window7-224.json'
}

def swin_hf_configs(model_type):
    global path_dict
    path_dict = dict_join_dirname(path_dict, os.path.dirname(__file__))
    return path_dict[model_type]

# ============= Set Model Config and Arguments =============
def set_model_config(config, args, overwrite_args=True):
    # ======= Arguments --> Model Config ======
    # Overwrite all model configs by manually set arguments
    if args.set_model_config_manually:
        config.drop_path_rate = args.drop_path_rate
        config.embed_dim = args.embed_dim
        config.depths = args.depths
        config.num_heads = args.num_heads
        config.window_size = args.window_size
        config.image_size = args.image_size
        config.patch_size = args.patch_size
        config.num_channels = args.num_channels
        config.num_classes = args.num_classes
        config.num_labels = args.num_classes # hardcoded here, shall adapt to dataset config if using real datasets
    # Overwrite layer number only
    elif args.set_layernum_manually:
        config.depths = args.depths
    
    # ======= Model Config --> Arguments ======
    # This step is necessary that maintains the consistency of model config and arguments.
    # Overwrite the model arguments with the model config
    overwrite_model_args(config, args)
    
    if overwrite_args: # Overwrite necessary Megatron-LM arguments with the model config
        overwrite_megatron_args(config, args)
    return config

def overwrite_megatron_args(config, args):
    args.num_layers = sum(config.depths)
    args.num_attention_heads = config.num_heads
    args.max_position_embeddings = config.embed_dim
    args.attention_dropout = config.attention_probs_dropout_prob
    args.hidden_dropout = config.hidden_dropout_prob
    args.use_cpu_initialization = True

# Need to overwrite the arguments with the model config
def overwrite_model_args(config, args):
    args.drop_path_rate = config.drop_path_rate
    args.embed_dim = config.embed_dim
    args.depths = config.depths
    args.num_heads = config.num_heads
    args.window_size = config.window_size
    args.image_size = config.image_size
    args.patch_size = config.patch_size
    args.num_channels = config.num_channels
    args.num_classes = config.num_labels

# ============= Get Model Name and Layer Configs =============
def head_name(num_heads):
    assert isinstance(num_heads, (tuple, list)) and len(num_heads) > 0
    str = f"{num_heads[0]}"
    for i in range(1, len(num_heads)):
        str += f",{num_heads[i]}"
    return '[' + str + ']'
        
def model_name(config, args=None):
    return 'embed%d_head%s_patch%d_window%d_img%d'%(
        config.embed_dim,
        head_name(config.num_heads),
        config.patch_size,
        config.window_size,
        config.image_size
    )

def model_layer_configs(config):
    return [
        {
            'hidden_size': config.embed_dim * (2**i),
            'seq_len': (config.image_size // config.patch_size // (2**i)) ** 2,
            'layer_num': config.depths[i]
        } for i in range(len(config.depths))
    ]