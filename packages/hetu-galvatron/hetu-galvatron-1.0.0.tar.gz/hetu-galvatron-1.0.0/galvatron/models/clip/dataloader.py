import torch
from torch.utils.data import Dataset
import numpy as np

# This is a simple random dataloader for CLIP!
class DataLoaderForCLIP(Dataset):
    def __init__(self, config, device):
        self.seq_len = config.text_config.max_position_embeddings
        self.image_size = config.vision_config.image_size
        self.vocab_size = config.text_config.vocab_size
        self.dataset_size = 2560*200
        self.input_ids = np.random.randint(0,self.vocab_size,(2, self.seq_len))
        self.attention_mask = np.random.randint(0,2,(2, self.seq_len))
        self.pixel_values = np.random.randint(0,256,(2, 3, self.image_size, self.image_size))
        self.device = device

    def __len__(self):
        return self.dataset_size

    def __getitem__(self, idx):
        if idx >= self.dataset_size:
            raise IndexError
        input_ids = torch.LongTensor(self.input_ids[0]).to(self.device)
        attention_mask = torch.Tensor(self.attention_mask[0]).to(self.device)
        pixel_values = torch.FloatTensor(self.pixel_values[0]).to(self.device)
        return input_ids, attention_mask, pixel_values