import torch
from torch import nn
import numpy as np
from transformers import ViTForImageClassification
from galvatron.core import construct_hybrid_parallel_model_api, get_hybrid_parallel_configs_api
from galvatron.models.vit.ViTModel_sequential import ViTModelInfo, construct_sequential_model
from galvatron.models.vit.ViTModel_tensor_parallel import construct_tensor_parallel_model, VitLayer_tp

def get_hybrid_parallel_configs(model_config, training_args):
    hybrid_parallel_configs = get_hybrid_parallel_configs_api(model_config, training_args, ViTModelInfo)
    return hybrid_parallel_configs

def construct_hybrid_parallel_model(model, model_config, training_args, hybrid_parallel_configs):
    wrap_block_name = [VitLayer_tp]
    hp_model = construct_hybrid_parallel_model_api(
        model,
        model_config,
        training_args,
        hybrid_parallel_configs,
        ViTModelInfo,
        construct_sequential_model,
        construct_tensor_parallel_model,
        wrap_block_name=wrap_block_name
    )
    return hp_model

def vit_model_hp(config, args):
    hybrid_parallel_configs = get_hybrid_parallel_configs(model_config=config, training_args=args)
    if args.local_rank == 0:
        print("Creating Model...")
    vit_model = ViTForImageClassification(config)
    model = construct_hybrid_parallel_model(
        model=vit_model, 
        model_config=config, 
        training_args=args, 
        hybrid_parallel_configs=hybrid_parallel_configs
    )
    return model