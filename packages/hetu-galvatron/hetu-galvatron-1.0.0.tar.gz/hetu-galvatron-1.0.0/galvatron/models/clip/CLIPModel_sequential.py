import torch.nn as nn
import torch
from typing import Any, Optional, Tuple, Union
from galvatron.core.pipeline import PipeSequential
from galvatron.core import mixed_precision_dtype, ModelInfo

# Copied from transformers.models.bart.modeling_bart._expand_mask
def _expand_mask(mask: torch.Tensor, dtype: torch.dtype, tgt_len: Optional[int] = None):
    """
    Expands attention_mask from `[bsz, seq_len]` to `[bsz, 1, tgt_seq_len, src_seq_len]`.
    """
    bsz, src_len = mask.size()
    tgt_len = tgt_len if tgt_len is not None else src_len

    expanded_mask = mask[:, None, None, :].expand(bsz, 1, tgt_len, src_len).to(dtype)

    inverted_mask = 1.0 - expanded_mask

    return inverted_mask.masked_fill(inverted_mask.to(torch.bool), torch.finfo(dtype).min)

# Copied from transformers.models.bart.modeling_bart._make_causal_mask
def _make_causal_mask(
    input_ids_shape: torch.Size, dtype: torch.dtype, device: torch.device, past_key_values_length: int = 0
):
    """
    Make causal mask used for bi-directional self-attention.
    """
    bsz, tgt_len = input_ids_shape
    mask = torch.full((tgt_len, tgt_len), torch.finfo(dtype).min, device=device)
    mask_cond = torch.arange(mask.size(-1), device=device)
    mask.masked_fill_(mask_cond < (mask_cond + 1).view(mask.size(-1), 1), 0)
    mask = mask.to(dtype)

    if past_key_values_length > 0:
        mask = torch.cat([torch.zeros(tgt_len, past_key_values_length, dtype=dtype, device=device), mask], dim=-1)
    return mask[None, None, :, :].expand(bsz, 1, tgt_len, tgt_len + past_key_values_length)

# contrastive loss function, adapted from
# https://sachinruk.github.io/blog/pytorch/pytorch%20lightning/loss%20function/gpu/2021/03/07/CLIP.html
def contrastive_loss(logits: torch.Tensor) -> torch.Tensor:
    return nn.functional.cross_entropy(logits, torch.arange(len(logits), device=logits.device))

def clip_loss(similarity: torch.Tensor) -> torch.Tensor:
    caption_loss = contrastive_loss(similarity)
    image_loss = contrastive_loss(similarity.t())
    return (caption_loss + image_loss) / 2.0

class CLIPVisionPreEncoder_(nn.Module):
    def __init__(self, model):
        super().__init__()
        attrs = ['embeddings', 'pre_layrnorm']
        for key in attrs:
            setattr(self, key, getattr(model.vision_model, key))
    def forward(self, input_ids, attention_mask, pixel_values):
        hidden_states = self.embeddings(pixel_values)
        hidden_states = self.pre_layrnorm(hidden_states)
        
        return input_ids, attention_mask, hidden_states

class CLIPTextPreEncoder_(nn.Module):
    def __init__(self, model):
        super().__init__()
        attrs = ['embeddings']
        for key in attrs:
            setattr(self, key, getattr(model.text_model, key))
    def forward(self, input_ids, attention_mask, image_embeds):
        input_shape = input_ids.size()
        input_ids = input_ids.view(-1, input_shape[-1])

        hidden_states = self.embeddings(input_ids=input_ids, position_ids=None)

        # CLIP's text model uses causal mask, prepare it here.
        # https://github.com/openai/CLIP/blob/cfcffb90e69f37bf2ff1e988237a0fbe41f33c04/clip/model.py#L324
        causal_attention_mask = _make_causal_mask(input_shape, hidden_states.dtype, device=hidden_states.device)
        input_ids = input_ids.clone()
        return input_ids, attention_mask, hidden_states, causal_attention_mask, image_embeds

class CLIPVisionEncoder_(nn.Module):
    def __init__(self, model, layer_idx_start, layer_idx_end):
        super().__init__()
        self.layers = model.vision_model.encoder.layers[layer_idx_start:layer_idx_end]

    def forward(self, input_ids, attention_mask, text_embeds, causal_attention_mask, image_embeds):
        hidden_states = image_embeds
        for idx, encoder_layer in enumerate(self.layers):
            layer_outputs = encoder_layer(
                hidden_states,
                attention_mask=None,
                causal_attention_mask=None,
                output_attentions=None,
            )
            hidden_states = layer_outputs[0]
        return input_ids, attention_mask, text_embeds, causal_attention_mask, hidden_states

class CLIPTextEncoder_(nn.Module):
    def __init__(self, model, layer_idx_start, layer_idx_end):
        super().__init__()
        self.layers = model.text_model.encoder.layers[layer_idx_start:layer_idx_end]

    def forward(self, input_ids, attention_mask, text_embeds, causal_attention_mask, image_embeds):
        hidden_states = text_embeds
        # expand attention_mask
        if attention_mask is not None:
            # [bsz, seq_len] -> [bsz, 1, tgt_seq_len, src_seq_len]
            # extended_attention_mask = _expand_mask(attention_mask, hidden_states.dtype)
            extended_attention_mask = _expand_mask(attention_mask, hidden_states.dtype)
        
        for idx, encoder_layer in enumerate(self.layers):
            layer_outputs = encoder_layer(
                hidden_states,
                attention_mask=extended_attention_mask,
                causal_attention_mask=causal_attention_mask,
                output_attentions=None,
            )
            hidden_states = layer_outputs[0]
        attention_mask = attention_mask.clone() if attention_mask is not None else None
        return input_ids, attention_mask, hidden_states, causal_attention_mask, image_embeds

class CLIPVisionPostEncoder_(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.post_layernorm = model.vision_model.post_layernorm
        self.visual_projection = model.visual_projection
        
    def forward(self, input_ids, attention_mask, text_embeds, causal_attention_mask, image_embeds):
        pooled_output = image_embeds[:, 0, :]
        pooled_output = self.post_layernorm(pooled_output)
        image_embeds = self.visual_projection(pooled_output)

        return input_ids, text_embeds, image_embeds

class CLIPTextPostEncoder_(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.final_layer_norm = model.text_model.final_layer_norm
        self.text_projection = model.text_projection
        
    def forward(self, input_ids, text_embeds, image_embeds):
        last_hidden_state = text_embeds
        last_hidden_state = self.final_layer_norm(last_hidden_state)

        # text_embeds.shape = [batch_size, sequence_length, transformer.width]
        # take features from the eot embedding (eot_token is the highest number in each sequence)
        # casting to torch.int for onnx compatibility: argmax doesn't support int64 inputs with opset 14
        
        pooled_output = last_hidden_state[
            torch.arange(last_hidden_state.shape[0], device=last_hidden_state.device),
            input_ids.to(dtype=torch.int, device=last_hidden_state.device).argmax(dim=-1),
        ]
        text_embeds = self.text_projection(pooled_output)

        return text_embeds, image_embeds

class CLIPCls_(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.logit_scale = model.logit_scale
        
    def forward(self, text_embeds, image_embeds):
        # normalized features
        image_embeds = image_embeds / image_embeds.norm(p=2, dim=-1, keepdim=True)
        text_embeds = text_embeds / text_embeds.norm(p=2, dim=-1, keepdim=True)

        # cosine similarity as logits
        logit_scale = self.logit_scale.exp()
        logits_per_text = torch.matmul(text_embeds, image_embeds.t()) * logit_scale
        # logits_per_image = logits_per_text.t()

        loss = clip_loss(logits_per_text)
        return loss

def construct_sequential_model(clip_model, config):
    model = PipeSequential()
    model.add_module('vision_embeddings', CLIPVisionPreEncoder_(clip_model))
    model.add_module('text_embeddings', CLIPTextPreEncoder_(clip_model))
    for i in range(config.vision_config.num_hidden_layers):
        enc = CLIPVisionEncoder_(clip_model, i, i + 1)
        model.add_module('vision_encoder_%d'%i, enc)
    for i in range(config.text_config.num_hidden_layers):
        enc = CLIPTextEncoder_(clip_model, i, i + 1)
        model.add_module('text_encoder_%d'%i, enc)
    model.add_module('vision_post', CLIPVisionPostEncoder_(clip_model))
    model.add_module('text_post', CLIPTextPostEncoder_(clip_model))
    
    model.add_module('cls', CLIPCls_(clip_model))
    return model

class CLIPModelInfo(ModelInfo):
    def __init__(self, config, args):
        super(CLIPModelInfo, self).__init__()
        layernum_list = [config.vision_config.num_hidden_layers, config.text_config.num_hidden_layers]
        mixed_precision = mixed_precision_dtype(args.mixed_precision)
        text_seq_len, img_seq_len = config.text_config.max_position_embeddings, (config.vision_config.image_size // config.vision_config.patch_size) ** 2 + 1
        text_hidden_size, img_hidden_size = config.text_config.hidden_size, config.vision_config.hidden_size
        layer_output_shape = [[-1, text_seq_len], [-1, text_seq_len], [-1, text_seq_len, text_hidden_size], [-1, 1, text_seq_len, text_seq_len], [-1, img_seq_len, img_hidden_size]]
        layer_output_dtype = [torch.long] + [mixed_precision] * 4
        layer_shapes_list = [layer_output_shape, layer_output_shape]
        layer_dtypes_list = [layer_output_dtype, layer_output_dtype]
        module_types = ['embed_vis', 'embed_text'] + ['clip_vis_enc']*config.vision_config.num_hidden_layers + ['clip_text_enc']*config.text_config.num_hidden_layers + ['vis_post', 'text_post', 'cls']
        self.set_layernums(layernum_list)
        self.set_shapes(layer_shapes_list)
        self.set_dtypes(layer_dtypes_list)
        self.set_module_types(module_types)