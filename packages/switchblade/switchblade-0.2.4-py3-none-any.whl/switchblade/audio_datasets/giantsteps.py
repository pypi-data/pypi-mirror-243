'''
The GTZAN dataset class, which extends the AudioDataset class
'''

from .dataset import Dataset
import json
import os
from typing import Callable, Optional

class GiantStepsDataset(Dataset):
    subsets = ['train', 'valid', 'test']
    n_outputs = 24
    
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
        '''
        dataroot: where the data exists; will recursively traverse
        subset: the subset to load
        return_labels: should labels be returned?
        labels: (filename : label) pairs or None if unlabeled
        n_samples: number of samples to return
        sr: which sample rate to use? will resample if necessary
        transform: optional transform to signal
        preprocess_path: path to store preprocessed data
        do_preprocessing: should we eagerly preprocess?
            'auto' = preprocess if necessary
        '''
        super().__init__()

        assert subset in self.subsets

        self.dataroot = dataroot 
        self.subset = subset
        self.return_labels = return_labels
        self.n_samples = n_samples
        self.sr = sr
        self.transform = transform
        self.filenames = []
        
        '''
        Annotations have them in 'sharp' while 'y' in dataset has them in 'flat' measure
        # means sharp
        C# = Db, D# = Eb, F# = Gb, G# = Ab, A# = Bb
        C sharp = D flat, D sharp = E flat
        '''
        self.classes = [
            'C Major','C Minor','Db Major','Db Minor','D Major',
            'D Minor','Eb Major','Eb Minor','E Major','E Minor',
            'F Major','F Minor','Gb Major','Gb Minor','G Major',
            'G Minor','Ab Major','Ab Minor','A Major','A Minor',
            'Bb Major','Bb Minor','B Major','B Minor'
        ]

        SPLIT_PATH = os.path.join(dataroot, 'giantsteps', 'giantsteps_clips.json')
        MUSIC_PATH = os.path.join(dataroot, 'giantsteps', 'audio')
        
        with open(SPLIT_PATH, 'r') as file :
            data = json.load(file)
              
        self.labels = {}
        
        '''
        Giantsteps split file has an odd structure so 
        test must be read differently than valid and train
        
        test = 604 songs
        train = 923 songs
        valid = 236 songs
        
        Dataset has more songs than are actually used in the subsets
        '''
        
        i = 0
        if subset == 'test':
            for key, entry in data.items():
                if entry.get('split') == subset and key.endswith('-0'):
                    Note = entry.get('y')
                    song = entry.get('extra').get('jams').get('file_metadata').get('title')
                    song = song[:-3] + 'mp3'
                    self.filenames.append(os.path.join(MUSIC_PATH,song))
                    self.labels[i] = Note 
                    i+=1
        else:
            for key, entry in data.items():
                if entry.get('split') == subset and key.endswith('-0'):
                    Note = entry.get('y')
                    song = entry.get('extra').get('beatport_metadata').get('ID')
                    song =  song + '.LOFI.mp3'
                    self.filenames.append(os.path.join(MUSIC_PATH,song))
                    self.labels[i] = Note 
                    i+=1

        self.labels[i] = Note # error handling

        for arg in kwargs.keys():
            if arg in self.VALID_KWARGS:
                self.__setattr__(arg, kwargs[arg])
            else:
                print(f'WARNING: {__class__.__name__} does not support "{arg}" argument.')

    def get_signal(self, i):
        filename = self.filenames[i]
        return self.load_signal(filename)
        
    def get_label(self, i):
        label = self.labels[i]
        return self.classes.index(label)
        
    def __len__(self):
        return len(self.filenames)