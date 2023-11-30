import torch
from torch.utils.data import Dataset
import h5py
import numpy as np

class DataLoaderForT5(Dataset):
    def __init__(self, args, device):
        file_path = "./data/train_data_"+args.model_size+".hdf5"
        f = h5py.File(file_path, "r")
        hdf5_keys = ['input_ids', 'attention_mask', 'labels']
        self.input_ids, self.attention_mask, self.labels =[np.tile(a, [16]+[1]*len(a.shape[1:])) for a in [np.asarray(f[key][:]) for key in hdf5_keys]]
        self.dataset_size = self.input_ids.shape[0]
        self.device = device
        f.close()

    def __len__(self):
        return self.dataset_size

    def __getitem__(self, idx):
        if idx >= self.dataset_size:
            raise IndexError
        input_ids = torch.LongTensor(self.input_ids[idx]).to(self.device)
        attention_mask = torch.LongTensor(self.attention_mask[idx]).to(self.device)
        labels = torch.LongTensor(self.labels[idx]).to(self.device)
        return input_ids, attention_mask, labels