from galvatron.core import initialize_galvatron, GalvatronSearchEngine
from galvatron.models.clip.arguments import model_args
from galvatron.models.clip.hf_configs import clip_hf_configs, set_model_config, model_name, model_layer_configs
from transformers import CLIPConfig
import os

if __name__ == '__main__':
    args = initialize_galvatron(model_args, mode='search')
    config = CLIPConfig.from_pretrained(clip_hf_configs(args.model_size))
    config = set_model_config(config, args)
    path = os.path.dirname(os.path.abspath(__file__))
    print(args)
    print(config)
    
    search_engine = GalvatronSearchEngine(args)
    search_engine.set_search_engine_info(path, model_layer_configs(config), model_name(config, args))
    search_engine.set_microbatch_func(microbatch_size=4, max_chunk=8) # Optional
    
    search_engine.initialize_search_engine()
    search_engine.check_cost_model(bsz=128)
    search_engine.parallelism_optimization()