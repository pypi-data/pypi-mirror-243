from transformers import SwinForImageClassification
from galvatron.core import construct_hybrid_parallel_model_api, get_hybrid_parallel_configs_api
from galvatron.models.swin.SwinModel_sequential import SwinModelInfo, construct_sequential_model
from galvatron.models.swin.SwinModel_tensor_parallel import construct_tensor_parallel_model, SwinBlock_tp

def get_hybrid_parallel_configs(model_config, training_args):
    hybrid_parallel_configs = get_hybrid_parallel_configs_api(model_config, training_args, SwinModelInfo)
    return hybrid_parallel_configs

def construct_hybrid_parallel_model(model, model_config, training_args, hybrid_parallel_configs):
    wrap_block_name = [SwinBlock_tp]
    hp_model = construct_hybrid_parallel_model_api(
        model,
        model_config,
        training_args,
        hybrid_parallel_configs,
        SwinModelInfo,
        construct_sequential_model,
        construct_tensor_parallel_model,
        wrap_block_name=wrap_block_name
    )
    return hp_model

def swin_model_hp(config, args):
    hybrid_parallel_configs = get_hybrid_parallel_configs(model_config=config, training_args=args)
    if args.local_rank == 0:
        print("Creating Model...")
    swin_model = SwinForImageClassification(config)
    model = construct_hybrid_parallel_model(
        model=swin_model, 
        model_config=config, 
        training_args=args, 
        hybrid_parallel_configs=hybrid_parallel_configs
    )
    return model