from pathlib import Path
import random
from typing import Callable, Optional

from . import constants
from .dataset import Dataset

class AudioDataset(Dataset):
    '''
    A generic audio dataset.

    dataroot: where the data exists; will recursively traverse
    return_labels: should labels be returned?
    labels: (filename : label) pairs or None if unlabeled
    n_samples: number of samples to return
    sr: which sample rate to use? will resample if necessary
    transform: optional transform to signal
    preprocess_path: path to store preprocessed data
    do_preprocessing: should we eagerly preprocess?
        'auto' = preprocess if necessary
    cap_at: should the dataset be 'capped' at a certain length? 
        Useful for testing data efficiency (i.e., sub-sampling data)
        So if cap_at is 100, this dataset will contain a random subset 
        of 100 audio files
    '''
    def __init__(
        self, 
        dataroot: str, 
        n_samples: Optional[int] = 50000, 
        sr: Optional[int] = 44100, 
        transform: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__()
        self.subsets = ['all']

        self.dataroot = dataroot
        self.n_samples = n_samples
        self.sr = sr
        self.transform = transform

        # collect a list of all filenames:
        self.filenames = []
        for extension in constants.SUPPORTED_FILETYPES:
            for filename in Path(dataroot).rglob(f'*.{extension}'):
                self.filenames.append(str(filename))
        random.shuffle(self.filenames)

        self.n_outputs = None

        for arg in kwargs.keys():
            if arg in self.VALID_KWARGS:
                self.__setattr__(arg, kwargs[arg])
            else:
                print(f'WARNING: {__class__.__name__} does not support "{arg}" argument.')

    def get_signal(self, i):
        try:
            filename = self.filenames[i]
            return self.load_signal(filename)
        except:
            return self.get_signal((i+1) % len(self))

    def get_label(self, i):
        return None

    def __len__(self):
        return len(self.filenames)