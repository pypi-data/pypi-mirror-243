'''
The DISCO Dataset: the largest available music dataset to date.
'''

from concurrent.futures import ThreadPoolExecutor
from .dataset import Dataset
from datasets import load_dataset
import hashlib
import os
import random
import re
import soundfile as sf
from tqdm import tqdm
from urllib.request import urlretrieve
from typing import Callable, Optional


class DISCOXDataset(Dataset):
    def __init__(
            self, 
            dataroot: str,
            n_samples: Optional[int] = 50000, 
            sr: Optional[int] = 44100, 
            transform: Optional[Callable] = None, 

            subset: str = '10k-random', 
            download: bool = False,

            chunk_dataset: bool = False,
            max_workers: int = 20, 
            dir_depth: int = 2,
            **kwargs
    ):
        super().__init__()

        self.return_same_slice = False
        self.return_same_slice_p = None
        self.subsets = ['10k-random', '200k-random', '200k-high-quality', '10m']
        self.dataset_name = {
            '10k-random' : 'DISCOX/DISCO-10K-random',
            '200k-random' : 'DISCOX/DISCO-200K-random',
            '200k-high-quality' : 'DISCOX/DISCO-200K-high-quality',
            '10m' : 'DISCOX/DISCO-10M'
        }[subset]
        self.dataroot = os.path.join(dataroot, 'DISCOX', subset)
        self.subset = subset
        self.max_workers = max_workers
        self.dir_depth = dir_depth
        self.n_outputs = None

        self.download_dataset = download
        self.n_samples = n_samples
        self.sr = sr
        self.transform = transform
        self.chunk_dataset = chunk_dataset

        # Load the dataset
        self.ds = load_dataset(self.dataset_name)
        self.urls = self.ds['train']['preview_url_spotify']

        # Ensure data is downloaded
        if not os.path.exists(self.dataroot) or self.download_dataset:
            print('Downloading/Verifying dataset...')
            self._ensure_data_downloaded()

        # Split data if requested (idea: to speed up training time)
        filename = self.url2filename(self.urls[0])
        hash_name = hashlib.md5(filename.encode()).hexdigest()
        sub_dirs = [self.dataroot] + [hash_name[i:i+2] for i in range(0, 2*self.dir_depth, 2)]
        base_filename = filename.split('.')[0]
        is_split = [f for f in os.listdir(os.path.join(*sub_dirs)) if base_filename in f and 'split' in f]
        if chunk_dataset and not is_split:
            try:
                self._split_data()
            except:
                print('Splitting was unsuccessful (probably a problem with the SoundFile library)')

        for arg in kwargs.keys():
            if arg in self.VALID_KWARGS:
                self.__setattr__(arg, kwargs[arg])
            else:
                print(f'WARNING: {__class__.__name__} does not support "{arg}" argument.')

    def _ensure_data_downloaded(self):
        os.makedirs(self.dataroot, exist_ok=True)

        def download_file(url):
            filename = self.url2filename(url)
            hash_name = hashlib.md5(filename.encode()).hexdigest()
            sub_dirs = [self.dataroot] + [
                hash_name[i:i+2] 
                for i in range(0, 2 * self.dir_depth, 2)
            ]
            sub_dir = os.path.join(*sub_dirs)
            os.makedirs(sub_dir, exist_ok=True)
            filename = os.path.join(sub_dir, filename)
            if not os.path.exists(filename) or (os.stat(filename).st_size == 0):
                try:
                    urlretrieve(url, filename)
                except Exception as e:
                    print(f'Failed to download: {url}\nError: {e}')

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            list(tqdm(executor.map(download_file, self.urls), total=len(self.urls)))

    def _split_file(self, url):
        '''
        Splits a single audio file into overlapping 2-second windows.
        '''
        window_size = self.sr * 2  # 2 seconds in samples
        hop_size = int(window_size / 2)  # 50% overlap

        filename = self.url2filename(url)
        hash_name = hashlib.md5(filename.encode()).hexdigest()
        sub_dirs = [self.dataroot] + [hash_name[i:i+2] for i in range(0, 2 * self.dir_depth, 2)]
        full_path = os.path.join(*sub_dirs, filename)
        
        signal, sr = sf.read(full_path)
        if len(signal.shape) > 1 and signal.shape[1] > 1:
            signal = signal.mean(axis=1)  # make mono

        # Calculate the number of splits based on hop size
        num_splits = int((len(signal) - window_size) / hop_size) + 1

        for i in range(num_splits):
            start_sample = i * hop_size
            end_sample = start_sample + window_size

            split_signal = signal[start_sample:end_sample]
            split_filename = f"{filename.split('.')[0]}_split_{i}.mp3"
            split_path = os.path.join(*sub_dirs, split_filename)

            sf.write(split_path, split_signal, sr)

    def _split_data(self):
        '''
        Splits each 30-second audio file into overlapping 2-second windows.
        '''
        print('Chunking dataset...')
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            list(tqdm(executor.map(self._split_file, self.urls), total=len(self.urls)))

    def get_signal(self, i: int):
        filename = self.url2filename(self.urls[i])
        hash_name = hashlib.md5(filename.encode()).hexdigest()
        sub_dirs = [self.dataroot] + [hash_name[i:i+2] for i in range(0, 2*self.dir_depth, 2)]

        base_filename = filename.split('.')[0]
        all_files = [f for f in os.listdir(os.path.join(*sub_dirs)) if base_filename in f and 'split' in f]
        if all_files:
            filename = random.choice(all_files)
        
        filename = os.path.join(*sub_dirs, filename)
        signal = self.load_signal(filename)

        return signal

    def get_label(self, i: int):
        # This is an unlabeled dataset
        return None

    def __len__(self):
        return len(self.urls)
    
    @staticmethod
    def url2filename(url):
        filename = url.split('/')[-1] + '.mp3'

        '''
        On Windows machines, certain non-alphanumeric characters that appear in these URLs
        cause problems, so we must sanitize the filenames first.
        '''
        return re.sub(r'[^\w.]+', '', filename)