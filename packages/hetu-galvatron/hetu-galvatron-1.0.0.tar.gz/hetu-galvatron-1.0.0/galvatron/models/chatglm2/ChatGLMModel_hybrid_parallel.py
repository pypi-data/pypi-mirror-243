import torch
from torch import nn
import numpy as np
from transformers import AutoModel
from galvatron.core import construct_hybrid_parallel_model_api, get_hybrid_parallel_configs_api
from galvatron.models.chatglm2.ChatGLMModel_sequential import ChatGLMModelInfo, construct_sequential_model
from galvatron.models.chatglm2.ChatGLMModel_tensor_parallel import construct_tensor_parallel_model, GLMBlock_tp

def get_hybrid_parallel_configs(model_config, training_args):
    hybrid_parallel_configs = get_hybrid_parallel_configs_api(model_config, training_args, ChatGLMModelInfo)
    return hybrid_parallel_configs

def construct_hybrid_parallel_model(model, model_config, training_args, hybrid_parallel_configs):
    # wrap_block_name = [GLMBlock_tp]
    wrap_block_name = None
    hp_model = construct_hybrid_parallel_model_api(
        model,
        model_config,
        training_args,
        hybrid_parallel_configs,
        ChatGLMModelInfo,
        construct_sequential_model,
        construct_tensor_parallel_model,
        wrap_block_name=wrap_block_name
    )
    return hp_model

def chatglm2_model_hp(config, args):
    hybrid_parallel_configs = get_hybrid_parallel_configs(model_config=config, training_args=args)
    if args.local_rank == 0:
        print("Creating Model...")
    chatglm2_model = AutoModel.from_config(config, trust_remote_code=True)
    model = construct_hybrid_parallel_model(
        model=chatglm2_model, 
        model_config=config, 
        training_args=args, 
        hybrid_parallel_configs=hybrid_parallel_configs
    )
    return model