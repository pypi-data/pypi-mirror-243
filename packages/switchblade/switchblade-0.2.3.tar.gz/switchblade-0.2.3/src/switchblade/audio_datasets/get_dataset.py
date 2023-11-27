'''
Quick and easy way to get any dataset
'''

from .audio_dataset import AudioDataset
from .discox import DISCOXDataset
from .emomusic import EmoMusicDataset
from .giantsteps import GiantStepsDataset
from .gtzan import GTZANDataset
from .magnatagatune import MagnaTagATuneDataset
from .nsynth import NSynthDataset

def set_default_backend():
    import os
    import torchaudio
    if os.name != 'nt':
        torchaudio.set_audio_backend('soundfile')

def get_dataset(dataset_name: str, set_backend: bool = True, **kwargs):
    if set_backend:
        set_default_backend()

    datasets = {
        'audio' : AudioDataset,
        'discox' : DISCOXDataset,
        'emomusic' : EmoMusicDataset,
        'giantsteps' : GiantStepsDataset,
        'gtzan' : GTZANDataset,
        'magnatagatune' : MagnaTagATuneDataset,
        'nsynth' : NSynthDataset
    }

    if dataset_name.lower() in datasets:
        return datasets[dataset_name](**kwargs)
    
    raise ValueError(f'Error: dataset {dataset_name} not found.')