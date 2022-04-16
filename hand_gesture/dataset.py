import numpy as np
import json

from torch.utils.data import Dataset, DataLoader

from config import data_path, class_names_to_idx


class HandGestureDataset(Dataset):

    def __init__(self, data_path='./data/dataset.json', dataset='train'):
        data = self.load_data(data_path=data_path)
        self.features = data[dataset]['features']
        self.labels = data[dataset]['labels']

    def __len__(self):
        return len(self.features)

    def __getitem__(self, index):
        feature = self.features[index]
        feature = np.array(feature, dtype=np.float32)
        label = self.labels[index]
        label = class_names_to_idx[label]
        label = np.array([0 if i != label else 1 for i in range(6)], dtype=np.float32)
        return feature, label

    def load_data(self, data_path):
        with open(data_path) as file:
            dataset = json.load(file)
        return dataset


def get_dataloader(data_path, batch_size):
    train_dataset = HandGestureDataset(data_path=data_path, dataset='train')
    val_dataset   = HandGestureDataset(data_path=data_path, dataset='test')
    train_dataloader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True,
                                  num_workers=0, pin_memory=True)
    val_dataloader   = DataLoader(dataset=val_dataset, batch_size=batch_size, shuffle=True,
                                  num_workers=0, pin_memory=True)
    return train_dataloader, val_dataloader


if __name__ == '__main__':
    get_dataloader(data_path=data_path, batch_size=4)
