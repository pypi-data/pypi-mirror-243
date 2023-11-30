import torch
from torch import nn
import numpy as np
from transformers import T5ForConditionalGeneration
from galvatron.core import construct_hybrid_parallel_model_api, get_hybrid_parallel_configs_api
from galvatron.models.t5.T5Model_sequential import T5ModelInfo, construct_sequential_model
from galvatron.models.t5.T5Model_tensor_parallel import construct_tensor_parallel_model, T5Block_tp

def get_hybrid_parallel_configs(model_config, training_args):
    hybrid_parallel_configs = get_hybrid_parallel_configs_api(model_config, training_args, T5ModelInfo)
    return hybrid_parallel_configs

def construct_hybrid_parallel_model(model, model_config, training_args, hybrid_parallel_configs):
    # wrap_block_name = [T5Block_tp]
    wrap_block_name = None
    hp_model = construct_hybrid_parallel_model_api(
        model,
        model_config,
        training_args,
        hybrid_parallel_configs,
        T5ModelInfo,
        construct_sequential_model,
        construct_tensor_parallel_model,
        wrap_block_name=wrap_block_name
    )
    return hp_model

def t5_model_hp(config, args):
    hybrid_parallel_configs = get_hybrid_parallel_configs(model_config=config, training_args=args)
    if args.local_rank == 0:
        print("Creating Model...")
    t5_model = T5ForConditionalGeneration(config)
    model = construct_hybrid_parallel_model(
        model=t5_model,
        model_config=config,
        training_args=args,
        hybrid_parallel_configs=hybrid_parallel_configs
    )
    return model