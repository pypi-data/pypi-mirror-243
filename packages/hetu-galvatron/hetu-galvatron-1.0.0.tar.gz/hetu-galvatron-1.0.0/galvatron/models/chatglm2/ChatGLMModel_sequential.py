import torch.nn as nn
import torch
from galvatron.core.pipeline import PipeSequential
from galvatron.core import mixed_precision_dtype, ModelInfo

class ChatGLMEmbeddings_(nn.Module):
    def __init__(self, config, model):
        super().__init__()
        self.config = config
        model = model.transformer
        self.embedding = model.embedding
        self.get_masks = model.get_masks
        self.rotary_pos_emb = model.rotary_pos_emb
        self.seq_length = model.seq_length
    
    def forward(self, input_ids, attention_mask=None):
        batch_size, seq_length = input_ids.shape

        inputs_embeds = self.embedding(input_ids).transpose(0, 1) # redo the transpose in self.embedding

        if attention_mask is not None and not attention_mask.all():
            full_attention_mask = self.get_masks(input_ids, None, padding_mask=attention_mask)

        # Rotary positional embeddings
        rotary_pos_emb = self.rotary_pos_emb(self.seq_length)
        rotary_pos_emb = rotary_pos_emb[None, :seq_length]
        # comment this line to remain the shape: [batch, seq_len]
        # rotary_pos_emb = rotary_pos_emb.transpose(0, 1).contiguous()
        
        hidden_states = inputs_embeds
        
        return hidden_states, full_attention_mask, rotary_pos_emb


class ChatGLMlayer_(nn.Module):
    def __init__(self, config, model, layer_idx):
        super().__init__()
        self.config = config
        self.layer_idx = layer_idx
        self.layer = model.transformer.encoder.layers[layer_idx]
    
    def forward(self, hidden_states, attention_mask, rotary_pos_emb):
        layer_ret = self.layer(
            hidden_states,
            attention_mask,
            rotary_pos_emb
        )
        hidden_states = layer_ret

        return hidden_states, attention_mask, rotary_pos_emb


class ChatGLMNorm_(nn.Module):
    def __init__(self, config, model):
        super().__init__()
        self.config = config
        self.post_layer_norm = config.post_layer_norm
        if self.post_layer_norm:
            self.final_layernorm = model.transformer.encoder.final_layernorm
    
    def forward(self, hidden_states, attention_mask, rotary_pos_emb):
        hidden_states = hidden_states.permute(1, 0, 2)
        hidden_states = self.final_layernorm(hidden_states)
        return hidden_states


class ChatGLMLMHead_(nn.Module):
    def __init__(self, config, model):
        super().__init__()
        self.config = config
        self.lm_head = model.transformer.output_layer

    def forward(self, hidden_states):
        lm_logits = self.lm_head(hidden_states).permute(1, 0, 2).contiguous()
        return lm_logits

def construct_sequential_model(model, config):
    model_ = PipeSequential()
    model_.add_module('embeddings', ChatGLMEmbeddings_(config, model))
    for i in range(config.num_layers):
        model_.add_module('encoder_%d'%i, ChatGLMlayer_(config, model, i))
    model_.add_module('norm', ChatGLMNorm_(config, model))
    model_.add_module('cls', ChatGLMLMHead_(config, model))
    return model_

class ChatGLMModelInfo(ModelInfo):
    def __init__(self, config, args):
        super(ChatGLMModelInfo, self).__init__()
        layernum_list = [config.num_layers]
        seq_len, hidden_size, kv_channels, mq_group_num = \
            config.seq_length, config.hidden_size, config.kv_channels, config.multi_query_group_num
        rotary_emb_dim = kv_channels // (2*mq_group_num) if config.multi_query_attention else kv_channels // 2
        mixed_precision = mixed_precision_dtype(args.mixed_precision)
        layer_shapes_list = [[[-1,seq_len,hidden_size], [-1,1,seq_len,seq_len], [-1,seq_len,rotary_emb_dim,2]]]
        layer_dtypes_list = [[mixed_precision, torch.bool, mixed_precision]]
        module_types = ['embed'] + ['chatglm2_enc']*config.num_layers + ['norm', 'cls']
        self.set_layernums(layernum_list)
        self.set_shapes(layer_shapes_list)
        self.set_dtypes(layer_dtypes_list)
        self.set_module_types(module_types)