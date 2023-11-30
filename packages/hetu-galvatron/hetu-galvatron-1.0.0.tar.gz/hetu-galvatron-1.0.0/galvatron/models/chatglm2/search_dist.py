from galvatron.core import initialize_galvatron, GalvatronSearchEngine
from galvatron.models.chatglm2.arguments import model_args
from galvatron.models.chatglm2.hf_configs import chatglm2_hf_configs, set_model_config, model_name, model_layer_configs
from transformers import AutoConfig
import os


if __name__ == '__main__':
    args = initialize_galvatron(model_args, mode='search')
    config = AutoConfig.from_pretrained(chatglm2_hf_configs(args.model_size), trust_remote_code=True)
    config = set_model_config(config, args, overwrite_args=False)
    path = os.path.dirname(os.path.abspath(__file__))
    print(args)
    print(config)
    
    search_engine = GalvatronSearchEngine(args)
    search_engine.set_search_engine_info(path, model_layer_configs(config), model_name(config))
    search_engine.set_microbatch_func(microbatch_size=4, max_chunk=8) # Optional
    # search_engine.set_model_type('bert') # Optional
    
    search_engine.initialize_search_engine()
    
    search_engine.parallelism_optimization()