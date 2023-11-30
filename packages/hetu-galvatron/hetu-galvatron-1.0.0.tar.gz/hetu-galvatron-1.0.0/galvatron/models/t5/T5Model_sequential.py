import torch.nn as nn
import torch
from torch import Tensor, device
from typing import Tuple
from galvatron.core.pipeline import PipeSequential
from galvatron.core import mixed_precision_dtype, ModelInfo

def get_extended_attention_mask_encoder(attention_mask: Tensor, input_shape: Tuple[int], device: device) -> Tensor:
    extended_attention_mask = attention_mask[:, None, None, :]
    extended_attention_mask = 1.0 - extended_attention_mask
    extended_attention_mask = extended_attention_mask.to(dtype=torch.bool)
    return extended_attention_mask

def get_extended_attention_mask_decoder(attention_mask: Tensor, input_shape: Tuple[int], device: device) -> Tensor:
    batch_size, seq_length = input_shape
    seq_ids = torch.arange(seq_length, device=device)
    causal_mask = seq_ids[None, None, :].repeat(batch_size, seq_length, 1) <= seq_ids[None, :, None]
    # in case past_key_values are used we need to add a prefix ones mask to the causal mask
    # causal and attention masks must have same type with pytorch version < 1.3
    causal_mask = causal_mask.to(attention_mask.dtype)

    if causal_mask.shape[1] < attention_mask.shape[1]:
        prefix_seq_len = attention_mask.shape[1] - causal_mask.shape[1]
        causal_mask = torch.cat(
            [
                torch.ones(
                    (batch_size, seq_length, prefix_seq_len), device=device, dtype=causal_mask.dtype
                ),
                causal_mask,
            ],
            axis=-1,
        )

    extended_attention_mask = causal_mask[:, None, :, :] * attention_mask[:, None, None, :]
    extended_attention_mask = 1.0 - extended_attention_mask
    extended_attention_mask = extended_attention_mask.to(dtype=torch.bool)
    return extended_attention_mask

def invert_attention_mask(encoder_attention_mask: Tensor) -> Tensor:
    encoder_extended_attention_mask = encoder_attention_mask[:, None, None, :]
    encoder_extended_attention_mask = 1.0 - encoder_extended_attention_mask
    encoder_extended_attention_mask = encoder_extended_attention_mask.to(dtype=torch.bool)
    return encoder_extended_attention_mask

class T5Embeddings_(nn.Module):
    def __init__(self, t5_model):
        super().__init__()
        self.embeddings = t5_model.shared
        self.dropout = t5_model.encoder.dropout

    def forward(self, input_ids, label, attention_mask):
        inputs_embeds = self.embeddings(input_ids)
        hidden_states = self.dropout(inputs_embeds)
        return hidden_states, label, attention_mask

class T5DecoderEmbedding_(nn.Module):
    def __init__(self, t5_model):
        super().__init__()
        self.embeddings = t5_model.shared
        self._shift_right = t5_model._shift_right
        self.dropout = t5_model.decoder.dropout

    def forward(self,  encoder_hidden_states, label, encoder_attention_mask):
        decoder_input_ids = self._shift_right(label)
        input_shape = decoder_input_ids.size()

        inputs_embeds = self.embeddings(decoder_input_ids)
        hidden_states = self.dropout(inputs_embeds)
        
        attention_mask = torch.ones(*input_shape).to(inputs_embeds.device)
        return encoder_hidden_states, encoder_attention_mask, hidden_states, attention_mask

class T5Encoder_(nn.Module):
    def __init__(self, t5_model, layer_idx, has_final_layernorm=False):
        super().__init__()
        self.dropout = t5_model.encoder.dropout
        self.block = t5_model.encoder.block[layer_idx]
        self.get_extended_attention_mask = t5_model.encoder.get_extended_attention_mask
        self.final_layernorm = t5_model.encoder.final_layer_norm if has_final_layernorm else None
    
    def forward(self, hidden_states, label, attention_mask, position_bias=None):
        extended_attention_mask = self.get_extended_attention_mask(attention_mask, attention_mask.shape, attention_mask.device)

        layer_outputs = self.block(
            hidden_states,
            attention_mask=extended_attention_mask,
            position_bias=position_bias
        )
        hidden_states = layer_outputs[0]
        
        if not self.final_layernorm is None:
            hidden_states = self.final_layernorm(hidden_states)
            hidden_states = self.dropout(hidden_states)
            return hidden_states, label, attention_mask
        
        return hidden_states, label, attention_mask

class T5Decoder_(nn.Module):
    def __init__(self, t5_model, layer_idx, has_final_layernorm=False):
        super().__init__()
        self.dropout = t5_model.decoder.dropout
        self.block = t5_model.decoder.block[layer_idx]
        self.get_extended_attention_mask = t5_model.decoder.get_extended_attention_mask
        self.invert_attention_mask = t5_model.decoder.invert_attention_mask
        self.final_layernorm = t5_model.decoder.final_layer_norm if has_final_layernorm else None
    
    def forward(self, encoder_hidden_states, encoder_attention_mask, hidden_states, attention_mask, position_bias=None, encoder_decoder_position_bias=None):
        extended_attention_mask = self.get_extended_attention_mask(attention_mask, attention_mask.shape, attention_mask.device)
        encoder_extended_attention_mask = self.invert_attention_mask(encoder_attention_mask)
        
        layer_outputs = self.block(
                hidden_states,
                attention_mask = extended_attention_mask,
                position_bias = position_bias,
                encoder_hidden_states = encoder_hidden_states,
                encoder_attention_mask = encoder_extended_attention_mask, 
                encoder_decoder_position_bias = encoder_decoder_position_bias
        )
        hidden_states = layer_outputs[0]
        
        if not self.final_layernorm is None:
            hidden_states = self.final_layernorm(hidden_states)
            hidden_states = self.dropout(hidden_states)
            return hidden_states

        return encoder_hidden_states, encoder_attention_mask, hidden_states, attention_mask

class T5Cls_(nn.Module):
    def __init__(self, t5_model):
        super().__init__()
        self.lm_head = t5_model.lm_head
        self.tie_word_embeddings = t5_model.config.tie_word_embeddings
        self.model_dim = t5_model.model_dim
    
    def forward(self, sequence_output):
        if self.tie_word_embeddings:
            sequence_output = sequence_output * (self.model_dim ** -0.5)

        lm_logits = self.lm_head(sequence_output)
        return lm_logits

def construct_sequential_model(model, config):
    model_ = PipeSequential()
    
    setattr(model.encoder, 'get_extended_attention_mask', get_extended_attention_mask_encoder)
    setattr(model.decoder, 'get_extended_attention_mask', get_extended_attention_mask_decoder)
    setattr(model.decoder, 'invert_attention_mask', invert_attention_mask)
    
    model_.add_module('embeddings_1', T5Embeddings_(model))
    for i in range(config.num_layers):
        model_.add_module('encoder_%d'%(i), T5Encoder_(model, i, has_final_layernorm= i + 1 >= config.num_layers))

    model_.add_module('embeddings_2', T5DecoderEmbedding_(model))
    for i in range(config.num_decoder_layers):
        model_.add_module('decoder_%d'%(i), T5Decoder_(model, i, has_final_layernorm= i + 1 >= config.num_decoder_layers))
    model_.add_module('cls', T5Cls_(model))
    return model_

class T5ModelInfo(ModelInfo):
    def __init__(self, config, args):
        super(T5ModelInfo, self).__init__()
        layernum_list = [config.num_layers, config.num_decoder_layers]
        seq_len, hidden_size = config.n_positions, config.d_model
        mixed_precision = mixed_precision_dtype(args.mixed_precision)
        layer_shapes_list = [
            [[-1,seq_len,hidden_size], [-1,seq_len], [-1,seq_len]],
            [[-1,seq_len,hidden_size], [-1,seq_len], [-1,seq_len,hidden_size], [-1,seq_len]]
        ]
        layer_dtypes_list = [
            [mixed_precision, torch.long, torch.long],
            [mixed_precision, torch.long, mixed_precision, torch.long]
        ]
        module_types = ['embed_1'] + ['t5_enc']*config.num_layers + ['embed_2'] + ['t5_dec']*config.num_decoder_layers + ['cls']
        self.set_layernums(layernum_list)
        self.set_shapes(layer_shapes_list)
        self.set_dtypes(layer_dtypes_list)
        self.set_module_types(module_types)