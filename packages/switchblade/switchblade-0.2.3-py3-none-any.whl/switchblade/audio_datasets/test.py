'''
Simple example for how to use this module
'''

from .get_dataset import get_dataset

dataset = get_dataset(
    dataset_name='discox',
    dataroot='/Users/oriyonay/Desktop/datasets',
    n_samples=50000,
    sr=16000,
    transform=None,
    subset='10k-random',
    download=False,
    return_labels=True,

    label_type='instrument_family',
    chunk_dataset=True,
    max_workers=20,
)

print(f'Created dataset with {len(dataset)} examples')
signal, label = dataset[0]
print(signal.shape, label)
dataset.return_labels = False
signal = dataset[0]
print(signal.shape)