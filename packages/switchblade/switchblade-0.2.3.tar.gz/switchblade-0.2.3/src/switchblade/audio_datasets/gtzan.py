'''
The GTZAN dataset class, which extends the AudioDataset class
'''

from .dataset import Dataset
import os
import json
import torch
from typing import Callable, Optional

class GTZANDataset(Dataset):
    subsets = ['train', 'valid', 'test']
    n_outputs = 10
    
    def __init__(
        self, 
        dataroot: str, 
        n_samples: Optional[int] = 50000, 
        sr: Optional[int] = 44100, 
        transform: Optional[Callable] = None,

        subset: str = 'train',
        return_labels: Optional[bool] = False,
        **kwargs
    ):
        super().__init__()
        
        assert subset in self.subsets
        
        self.dataroot = dataroot 
        self.subset = subset
        self.return_labels = return_labels
        self.n_samples = n_samples
        self.sr = sr
        self.transform = transform
        self.filenames = []

        self.classes = [
            'pop', 'metal', 'disco', 'blues', 
            'reggae', 'classical', 'rock', 'hiphop', 
            'country', 'jazz'
        ]

        SPLIT_PATH = os.path.join(dataroot, 'gtzan', 'gtzan_ff.json')
        MUSIC_PATH = os.path.join(dataroot, 'gtzan', 'genres_original')
        
        with open(SPLIT_PATH, 'r') as file:
            data = json.load(file)
              
        self.labels = {}
        for entry in data.values():
            if entry.get('split') == subset:
                genre = entry.get('y')
                song = entry.get('extra').get('id') + '.wav'
                self.filenames.append(os.path.join(MUSIC_PATH,genre,song))
                self.labels[os.path.join(MUSIC_PATH,genre,song)] = genre 

        for arg in kwargs.keys():
            if arg in self.VALID_KWARGS:
                self.__setattr__(arg, kwargs[arg])
            else:
                print(f'WARNING: {__class__.__name__} does not support "{arg}" argument.')

    def get_signal(self, i):
        filename = self.filenames[i]
        try:
            return self.load_signal(filename)
        except Exception:
            print(f'Error loading {filename}; returning empty signal to avoid crashing')
            return torch.zeros(self.n_samples)

    def get_label(self, i):
        label = self.labels[self.filenames[i]]
        return self.classes.index(label)

    def __len__(self):
        return len(self.filenames)
