import torch
from torch.utils.data import Dataset
import h5py
import numpy as np

class DataLoaderForViT(Dataset):
    def __init__(self, config, device):
        self.num_classes = config.num_labels
        self.num_channels = config.num_channels
        self.image_size = config.image_size
        self.dataset_size = 2560 * 16
        self.device = device

        self.pixel_values, self.labels = [], []
        for i in range(self.dataset_size):
            pixel_values = np.random.rand(self.num_channels, self.image_size, self.image_size)
            label = np.random.randint(0, self.num_classes, (1,))
            
            self.pixel_values.append(pixel_values)
            self.labels.append(label)
        
        self.pixel_values = np.array(self.pixel_values)
        self.labels = np.array(self.labels)

    def __len__(self):
        return self.dataset_size

    def __getitem__(self, idx):
        if idx >= self.dataset_size:
            raise IndexError
        pixel_values = torch.Tensor(self.pixel_values[idx]).to(self.device)
        labels = torch.LongTensor(self.labels[idx]).to(self.device)
        return pixel_values, labels