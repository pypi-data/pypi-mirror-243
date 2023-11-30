from abc import abstractmethod
import math
import random

import numpy as np
import soundfile as sf
import torch
import torchaudio
from torchaudio import transforms
from torch.utils.data import Dataset as TorchDataset

class Dataset(TorchDataset):
    '''
    The abstract dataset class definition.
    All of these functions take 1d signal input (i.e., shape is (n,)) and 
    produce 1d output - including self.get_signal().
    '''

    VALID_KWARGS = [
        'n_outputs',
        'n_views',
        'return_same_slice',
        'return_same_slice_p',
        'subsets',
        'return_labels',
        'n_views',
        'return_as_is',
        'return_same_slice',
        'return_same_slice_p',
        'return_index',
        'transform'
    ]

    @abstractmethod
    def __init__(self):
        '''
        the Dataset class should create the following:

        self.get_signal, self.get_label, self._sanity_check, and self.__len__ functions
        self.return_labels: bool
        self.n_samples: int
        self.sr: int
        self.transform: callable
        self.preprocess_path: str
        self.n_outputs: None if unlabeled, int otherwise (number of classes/outputs)
        self.n_views: int; default = 2
        self.return_same_slice: bool; default = False
        self.return_same_slice_p: float in [0, 1]; default = None
        self.subsets: list of strings of all subset names (ex. ['train', 'val', 'test'])
        '''
        
        self.return_labels = False # default; child instances can change this
        self.n_views = 1
        self.return_as_is = False
        self.return_same_slice = False
        self.return_same_slice_p = None
        self.dir_depth = 2
        self.return_index = False
        self.transform = None
        
    @abstractmethod
    def get_signal(self, i: int):
        '''
        returns signal for the ith datapoint. 
        should return a tensor of shape (n,) (i.e., no stereo -
        can use self.make_mono_if_necessary())
        '''
        pass

    @abstractmethod
    def get_label(self, i: int):
        '''
        returns the label for the ith datapoint
        '''
        pass

    @abstractmethod
    def __len__(self):
        pass

    def load_signal(self, filename):
        signal, sr = torchaudio.load(filename)
        
        # error handling: in case torchaudio returns an empty file
        if signal.numel() == 0:
            signal, sr = sf.read(filename)
            signal = torch.tensor(signal, dtype=torch.float32) # (n_samples, n_channels)
            if signal.dim() == 1: signal = signal.unsqueeze(1)
            signal = signal.mT # (n_channels, n_samples)
            
        signal = self.make_mono_if_necessary(signal)
        signal = self.resample_if_necessary(signal, sr)
        return signal

    def slice_signal(self, signal):
        assert len(signal.shape) == 1
        max_start_idx = len(signal) - self.n_samples

        if max_start_idx < 0:
            # how many times do we need to repeat the signal?
            n_repeat = math.ceil(self.n_samples / len(signal))
            signal = signal.repeat(n_repeat)
            max_start_idx = len(signal) - self.n_samples

        start_idx = random.randrange(max_start_idx) if max_start_idx != 0 else 0
        return signal[start_idx : start_idx + self.n_samples]
    
    def resample_if_necessary(self, signal, sr):
        if len(signal.shape) == 1: 
            signal = signal.unsqueeze(0)
        else: 
            raise ValueError('Signal must be one-dimensional.')

        if (self.sr is not None) and (sr != self.sr):
            resampler = transforms.Resample(orig_freq=sr, new_freq=self.sr)
            signal = resampler(signal)
        return signal.squeeze()
    
    def make_mono_if_necessary(self, signal):
        # return shape: (n,)
        if signal.dim() == 1: 
            return signal
        if signal.dim() == 2:
            return signal.mean(axis=0)
        raise ValueError('Signal must be 1d or 2d.')

    def __getitem__(self, i: int):
        signal = self.get_signal(i)
        label = self.get_label(i)

        if self.return_as_is:
            data = [signal]
            if self.return_labels:
                data.append(label)
            if self.return_index:
                data.append(i)
            return data if len(data) > 1 else data[0]

        # with probability p, return the same slice
        if self.return_same_slice_p:
            return_same_slice = np.random.random() < self.return_same_slice_p
        else:
            return_same_slice = self.return_same_slice

        if return_same_slice:
            signal = self.slice_signal(signal)

        views = []
        for j in range(self.n_views):
            # signal already loaded on first iteration
            if j != 0 and not self.return_same_slice:
                signal = self.get_signal(j)

            view = self.slice_signal(signal).unsqueeze(0)
            if self.transform:
                view = self.transform(view)
            views.append(view)

        data = views
        if self.return_labels:
            data.append(label)
        if self.return_index:
            data.append(i)

        return data if len(data) > 1 else data[0]