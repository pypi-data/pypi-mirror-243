from galvatron.core import GalvatronProfiler, initialize_galvatron
from galvatron.models.t5.arguments import model_args, layernum_arg_names
from galvatron.models.t5.hf_configs import t5_hf_configs, set_model_config, model_name
from transformers import T5Config
import os

if __name__ == "__main__":
    args = initialize_galvatron(model_args, mode="profile")
    config = T5Config.from_pretrained(t5_hf_configs(args.model_size))
    config = set_model_config(config, args, overwrite_args=False)
    
    profiler = GalvatronProfiler(args)
    path = os.path.dirname(os.path.abspath(__file__))
    profiler.set_profiler_launcher(path, layernum_arg_names(), model_name(config))
    
    profiler.launch_profiling_scripts()
    profiler.process_profiled_data()