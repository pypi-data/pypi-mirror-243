import json
import os
from pathlib import Path
import tarfile
from typing import Callable, Optional

from .dataset import Dataset
from .utils import download_file

URLS = {
    'train' : 'http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-train.jsonwav.tar.gz',
    'valid' : 'http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-valid.jsonwav.tar.gz',
    'test'  : 'http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-test.jsonwav.tar.gz'
}

class NSynthDataset(Dataset):
    subsets = ['train', 'valid', 'test']
    
    '''
    The NSynth Dataset class.

    dataroot: where the data exists/where to download it
    subset: train/test/valid
    download: should the dataset be downloaded?
    return_labels: should labels be returned?
    label_type: which label type should be returned?
    n_samples: number of samples to return
    sr: which sample rate to use? will resample if necessary
    transform: optional transform to signal
    '''
    def __init__(
        self, 
        dataroot: str, 
        n_samples: Optional[int] = 50000, 
        sr: Optional[int] = 44100, 
        transform: Optional[Callable] = None, 
        subset: str = 'train', 
        download: Optional[bool] = False, 
        return_labels: Optional[bool] = True, 
        label_type: Optional[bool] = 'instrument_family',
        **kwargs
    ):
        super().__init__()
        
        # assert subset in self.subsets
        assert label_type in [
            'instrument_family', 
            'qualities', 
            'instrument_source',
            'pitch'
        ]

        self.dataroot = dataroot
        self.subset = subset
        self.download = download
        self.return_labels = return_labels
        self.label_type = label_type
        self.n_samples = n_samples
        self.sr = sr
        self.transform = transform
        self.n_outputs = {
            'instrument_family' : 11,
            'pitch' : 128,
            'qualities' : 10,
            'instrument_source' : 3
        }[label_type]

        path = os.path.join(dataroot, f'nsynth-{subset}')
        if download and not os.path.exists(path):
            print('downloading dataset...')
            Path(dataroot).mkdir(parents=True, exist_ok=True)
            filename = os.path.basename(URLS[subset])
            filename = download_file(URLS[subset], os.path.join(dataroot, filename))

            print('downloaded dataset. unzipping...')
            with tarfile.open(filename) as f:
                f.extractall(dataroot)
            os.remove(filename)

        # get a list of all filenames:
        self.filenames = os.listdir(os.path.join(path, 'audio'))
        self.filenames = list(filter(lambda x: x.endswith('wav'), self.filenames))
        self.filenames = [os.path.join(path, 'audio', filename) for filename in self.filenames]

        # get the labels:
        self.labels = json.load(open(os.path.join(path, 'examples.json')))
        assert len(self.labels) == len(self.filenames)

        for arg in kwargs.keys():
            if arg in self.VALID_KWARGS:
                self.__setattr__(arg, kwargs[arg])
            else:
                print(f'WARNING: {__class__.__name__} does not support "{arg}" argument.')

    def get_signal(self, i):
        filename = self.filenames[i]
        return self.load_signal(filename)

    def get_label(self, i):
        # get just the entry filename (without extension):
        filename = self.filenames[i]
        entry = os.path.basename(filename).rsplit('.', 1)[0]

        entry = self.labels[entry]
        label = entry[self.label_type]

        return label

    def __len__(self):
        return len(self.filenames)