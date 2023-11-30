import torch
from torch.utils.data import Dataset
import h5py
import numpy as np

class DataLoaderForChatGLM2(Dataset):
    def __init__(self, config, device):
        self.vocab_size = config.padded_vocab_size
        self.sentence_length = config.seq_length
        self.dataset_size = 2560 * 16
        self.data_length = np.random.randint(self.sentence_length//8,self.sentence_length,(self.dataset_size,))
        self.device = device

        self.input_ids, self.attention_mask, self.labels = [], [], []
        for i in range(self.dataset_size):
            sentence = np.random.randint(0,self.vocab_size,(self.sentence_length,))
            sentence[self.data_length[i]:] = config.pad_token_id
            
            mask = np.ones((self.sentence_length,))
            mask[self.data_length[i]:] = 0

            label = sentence.copy()
            mask_position = np.random.randint(1, self.data_length[i])
            label[mask_position] = -100
            
            self.input_ids.append(sentence)
            self.attention_mask.append(mask)
            self.labels.append(label)
        
        self.input_ids = np.array(self.input_ids)
        self.attention_mask = np.array(self.attention_mask)
        self.labels = np.array(self.labels)

    def __len__(self):
        return self.dataset_size

    def __getitem__(self, idx):
        if idx >= self.dataset_size:
            raise IndexError
        input_ids = torch.LongTensor(self.input_ids[idx]).to(self.device)
        attention_mask = torch.LongTensor(self.attention_mask[idx]).to(self.device)
        labels = torch.LongTensor(self.labels[idx]).to(self.device)
        return input_ids, attention_mask, labels