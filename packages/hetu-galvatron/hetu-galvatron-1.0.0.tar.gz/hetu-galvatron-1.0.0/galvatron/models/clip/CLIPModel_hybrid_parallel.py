from transformers import CLIPModel
from transformers.models.clip.modeling_clip import CLIPEncoderLayer
from galvatron.core import construct_hybrid_parallel_model_api, get_hybrid_parallel_configs_api
from galvatron.models.clip.CLIPModel_sequential import CLIPModelInfo, construct_sequential_model
from galvatron.models.clip.CLIPModel_tensor_parallel import construct_tensor_parallel_model

def get_hybrid_parallel_configs(model_config, training_args):
    hybrid_parallel_configs = get_hybrid_parallel_configs_api(model_config, training_args, CLIPModelInfo)
    return hybrid_parallel_configs

def construct_hybrid_parallel_model(model, model_config, training_args, hybrid_parallel_configs):
    wrap_block_name = [CLIPEncoderLayer]
    hp_model = construct_hybrid_parallel_model_api(
        model,
        model_config,
        training_args,
        hybrid_parallel_configs,
        CLIPModelInfo,
        construct_sequential_model,
        construct_tensor_parallel_model,
        wrap_block_name=wrap_block_name
    )
    return hp_model

def clip_model_hp(config, args):
    hybrid_parallel_configs = get_hybrid_parallel_configs(model_config=config, training_args=args)
    if args.local_rank == 0:
        print("Creating Model...")
    clip_model = CLIPModel(config)
    model = construct_hybrid_parallel_model(
        model=clip_model, 
        model_config=config, 
        training_args=args, 
        hybrid_parallel_configs=hybrid_parallel_configs
    )
    return model