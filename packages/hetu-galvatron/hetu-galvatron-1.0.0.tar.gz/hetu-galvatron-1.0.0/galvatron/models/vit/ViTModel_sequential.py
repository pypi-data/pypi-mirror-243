import torch.nn as nn
import torch
from galvatron.core.pipeline import PipeSequential
from galvatron.core import mixed_precision_dtype, ModelInfo

class VitEmbedding_(nn.Module):
    def __init__(self, vit_model):
        super().__init__()
        self.embedding = vit_model.vit.embeddings

    def forward(self, pixel_value):
        embedding_output = self.embedding(pixel_value)
        return embedding_output

class VitEncoder_(nn.Module):
    def __init__(self, vit_model, layer_idx_start, layer_idx_end):
        super().__init__()
        self.layer = vit_model.vit.encoder.layer[layer_idx_start: layer_idx_end]
    
    def forward(self, hidden_states):
        for i, layer_module in enumerate(self.layer):
            layer_outputs = layer_module(hidden_states, None, None)
            hidden_states = layer_outputs[0]

        return hidden_states

class VitLayerNorm_(nn.Module):
    def __init__(self, vit_model):
        super().__init__()
        self.layernorm = vit_model.vit.layernorm

    def forward(self, input):
        output = self.layernorm(input)
        return output[:, 0, :]

class VitCls_(nn.Module):
    def __init__(self, vit_model):
        super().__init__()
        self.classifier = vit_model.classifier

    def forward(self, input):
        output = self.classifier(input)
        return output

def construct_sequential_model(model, config):
    model_ = PipeSequential()
    model_.add_module('embedding', VitEmbedding_(model))
    for i in range(config.num_hidden_layers):
        model_.add_module('encoder_%d'%(i), VitEncoder_(model, i, i + 1))
    model_.add_module('layernorm', VitLayerNorm_(model))
    model_.add_module('cls', VitCls_(model))
    return model_

class ViTModelInfo(ModelInfo):
    def __init__(self, config, args):
        super(ViTModelInfo, self).__init__()
        layernum_list = [config.num_hidden_layers]
        seq_len, hidden_size = (config.image_size // config.patch_size) ** 2 + 1, config.hidden_size
        mixed_precision = mixed_precision_dtype(args.mixed_precision)
        layer_shapes_list = [[[-1,seq_len,hidden_size]]]
        layer_dtypes_list = [[mixed_precision]]
        module_types = ['embed'] + ['vit_enc']*config.num_hidden_layers + ['layernorm', 'cls']
        self.set_layernums(layernum_list)
        self.set_shapes(layer_shapes_list)
        self.set_dtypes(layer_dtypes_list)
        self.set_module_types(module_types)