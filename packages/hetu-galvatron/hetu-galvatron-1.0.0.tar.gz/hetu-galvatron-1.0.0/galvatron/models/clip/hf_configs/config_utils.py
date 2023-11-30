import os
from galvatron.utils import dict_join_dirname

# ============= HuggingFace Model Config Paths =============
path_dict =  {
    'vit-B-16': 'CLIP-ViT-B-16.json',
    'vit-L-14': 'CLIP-ViT-L-14-laion2B-s32B-b82K.json',
    'vit-H-14': 'CLIP-ViT-H-14-laion2B-s32B-b79K.json',
    'vit-g-14': 'CLIP-ViT-g-14-laion2B-s12B-b42K.json',
    'vit-bigG-14': 'CLIP-ViT-bigG-14-laion2B-39B-b160k.json',
}

def clip_hf_configs(model_type):
    global path_dict
    path_dict = dict_join_dirname(path_dict, os.path.dirname(__file__))
    return path_dict[model_type]

# ============= Set Model Config and Arguments =============
def set_model_config(config, args):
    # ======= Arguments --> Model Config ======
    # Overwrite all model configs by manually set arguments
    if args.set_model_config_manually or args.set_layernum_manually:
        config.text_config.num_hidden_layers = args.num_hidden_layers_text
        config.vision_config.num_hidden_layers = args.num_hidden_layers_vision
    
    # ======= Model Config --> Arguments ======
    # This step is necessary that maintains the consistency of model config and arguments.
    # Overwrite the model arguments with the model config
    overwrite_model_args(config, args)
    return config

# Need to overwrite the arguments with the model config
def overwrite_model_args(config, args):
    args.num_hidden_layers_text = config.text_config.hidden_size
    args.num_hidden_layers_vision = config.vision_config.hidden_size

# ============= Get Model Name and Layer Configs =============
def model_name(config, args=None):
    return 'CLIP-%s'%args.model_size

def model_layer_configs(config):
    vision_cfg = {
            'hidden_size': config.vision_config.hidden_size,
            'seq_len': (config.vision_config.image_size // config.vision_config.patch_size) ** 2 + 1,
            'layer_num': config.vision_config.num_hidden_layers
        }
    text_cfg = {
            'hidden_size': config.text_config.hidden_size,
            'seq_len': config.text_config.max_position_embeddings,
            'layer_num': config.text_config.num_hidden_layers
        }
    return [vision_cfg, text_cfg]