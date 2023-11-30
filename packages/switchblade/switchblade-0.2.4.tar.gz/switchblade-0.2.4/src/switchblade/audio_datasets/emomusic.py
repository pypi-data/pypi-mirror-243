from .dataset import Dataset
import json
import os
import torch
from typing import Callable, Optional

class EmoMusicDataset(Dataset):
    
    '''
    Makes the assumption that all dataset audio files are in their respective audio folders.
    This Dataset consists Specifically of mp3 files. There should be 1000 audio files,
    although only 744 as there are duplicates.
    '''
    subsets = ['train', 'valid', 'test']
    n_outputs = 2
    
    def __init__(
        self,
        dataroot: str,
        n_samples: Optional[int] = 50000, 
        sr: Optional[int] = 44100, 
        transform: Optional[Callable] = None, 
        subset: Optional[str] = None,
        return_labels: bool = False,
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
        self._path = os.path.join(dataroot, 'emomusic') 
        self.filenames = [] 
        self.labels = {}
        
        if not os.path.isdir(self._path):
            raise RuntimeError(
                'Dataset not found. Please go to https://cvml.unige.ch/databases/emoMusic/ and fill out the google doc to get access.'
            )
            
        SPLIT_PATH = os.path.join(self._path,'emomusic.json')
        MUSIC_PATH = os.path.join(self._path, 'clips_45seconds')
        
        with open(SPLIT_PATH, 'r') as file:
            data = json.load(file)

        for key, entry in data.items():
            if isinstance(entry, dict) and entry['split'] == subset:
                song = str(int(key))
                self.labels[song] = entry['y']
                self.filenames.append(os.path.join(MUSIC_PATH, song + '.mp3'))

        for arg in kwargs.keys():
            if arg in self.VALID_KWARGS:
                self.__setattr__(arg, kwargs[arg])
            else:
                print(f'WARNING: {__class__.__name__} does not support "{arg}" argument.')
        
    def get_signal(self, i: int):
        filename = self.filenames[i]
        return self.load_signal(filename)

    def get_label(self, i):
        # gets the filename without extension
        song_key = os.path.basename(self.filenames[i]).split('.')[0]
        return torch.FloatTensor(self.labels[song_key])

    def __len__(self):
        return len(self.filenames)