import torch.nn as nn
import torch
from galvatron.core.pipeline import PipeSequential
from galvatron.core import mixed_precision_dtype, ModelInfo

class SwinEmbeddings_(nn.Module):
    def __init__(self, swin_model):
        super().__init__()
        self.embeddings = swin_model.swin.embeddings
    
    def forward(self, pixel_value):
        outputs = self.embeddings(pixel_value)
        return outputs[0]

class SwinBlock_(nn.Module):
    def __init__(self, swin_model, layer_idx, block_idx, has_downsample=False):
        super().__init__()
        layer = swin_model.swin.encoder.layers[layer_idx]

        self.block = layer.blocks[block_idx]
        self.downsamlpe = layer.downsample if has_downsample else None
    
    def forward(self, hidden_states):
        layer_outputs = self.block(hidden_states, None, False)
        hidden_states = layer_outputs[0]
        if self.downsamlpe is not None:
            hidden_states = self.downsamlpe(hidden_states, self.downsamlpe.input_resolution)
        return hidden_states

class SwinLayernorm_(nn.Module):
    def __init__(self, swin_model):
        super().__init__()
        self.layernorm = swin_model.swin.layernorm
    
    def forward(self, hidden_states):
        sequence_output = self.layernorm(hidden_states)
        return sequence_output

class SwinCls_(nn.Module):
    def __init__(self, swin_model):
        super().__init__()
        self.pooler = swin_model.swin.pooler
        self.classifier = swin_model.classifier
    
    def forward(self, sequence_output):

        if self.pooler is not None:
            pooled_output = self.pooler(sequence_output.transpose(1, 2))
            pooled_output = torch.flatten(pooled_output, 1)
        
        logits = self.classifier(pooled_output)
        return logits

def construct_sequential_model(model, config):
    model_ = PipeSequential()
    model_.add_module('embeddings', SwinEmbeddings_(model))

    for i, d in enumerate(config.depths):
        for j in range(d):
            model_.add_module('encoder_%d_%d'%(i, j), SwinBlock_(model, i, j, j==d-1))
    
    model_.add_module('layernorm', SwinLayernorm_(model))
    model_.add_module('cls', SwinCls_(model))
    return model_

class SwinModelInfo(ModelInfo):
    def __init__(self, config, args):
        super(SwinModelInfo, self).__init__()
        mixed_precision = mixed_precision_dtype(args.mixed_precision)
        layernum_list = []
        layer_shapes_list = []
        layer_dtypes_list = []
        for i in range(len(config.depths)):
            seq_len, hidden_size = (config.image_size // config.patch_size // (2**i)) ** 2, config.embed_dim * (2**i)
            layer_shapes_list += [[[-1,seq_len,hidden_size]]]
            layer_dtypes_list += [[mixed_precision]]
            if i < len(config.depths) -1: # downsample
                layernum_list += [config.depths[i]-1, 1]
                layer_shapes_list += [[[-1,seq_len//4,hidden_size*2]]]
                layer_dtypes_list += [[mixed_precision]]
            else:
                layernum_list += [config.depths[i]]
        module_types = ['embed'] + ['swin_enc']*sum(config.depths) + ['pooler', 'cls']
        self.set_layernums(layernum_list)
        self.set_shapes(layer_shapes_list)
        self.set_dtypes(layer_dtypes_list)
        self.set_module_types(module_types)