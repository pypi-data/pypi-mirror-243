'''
Audio augmentation code :)
'''

import numpy as np
import random
from torch_audiomentations import *

import torch
from torch import Tensor
from torch_audiomentations.core.transforms_interface import BaseWaveformTransform
from torch_audiomentations.utils.object_dict import ObjectDict
from typing import Optional

# SpliceOut code is a paste from torch_audiomentations because it's not "officially" in yet.
class SpliceOut(BaseWaveformTransform):
    """
    spliceout augmentation proposed in https://arxiv.org/pdf/2110.00046.pdf
    silence padding is added at the end to retain the audio length.
    """
    supported_modes = {"per_batch", "per_example"}
    requires_sample_rate = True

    def __init__(
        self,
        num_time_intervals=8,
        max_width=400,
        mode: str = "per_example",
        p: float = 0.5,
        p_mode: Optional[str] = None,
        sample_rate: Optional[int] = None,
        target_rate: Optional[int] = None,
        output_type: Optional[str] = None,
    ):
        """
        param num_time_intervals: number of time intervals to spliceout
        param max_width: maximum width of each spliceout in milliseconds
        param n_fft: size of FFT
        """

        super().__init__(
            mode=mode,
            p=p,
            p_mode=p_mode,
            sample_rate=sample_rate,
            target_rate=target_rate,
            output_type=output_type,
        )
        self.num_time_intervals = num_time_intervals
        self.max_width = max_width

    def randomize_parameters(
        self,
        samples: Tensor = None,
        sample_rate: Optional[int] = None,
        targets: Optional[Tensor] = None,
        target_rate: Optional[int] = None,
    ):

        self.transform_parameters["splice_lengths"] = torch.randint(
            low=0,
            high=int(sample_rate * self.max_width * 1e-3),
            size=(samples.shape[0], self.num_time_intervals),
        )

    def apply_transform(
        self,
        samples: Tensor = None,
        sample_rate: Optional[int] = None,
        targets: Optional[Tensor] = None,
        target_rate: Optional[int] = None,
    ) -> ObjectDict:

        spliceout_samples = []

        for i in range(samples.shape[0]):

            random_lengths = self.transform_parameters["splice_lengths"][i]
            sample = samples[i][:, :]
            for j in range(self.num_time_intervals):
                start = torch.randint(
                    0,
                    sample.shape[-1] - random_lengths[j],
                    size=(1,),
                )

                if random_lengths[j] % 2 != 0:
                    random_lengths[j] += 1

                hann_window_len = random_lengths[j]
                hann_window = torch.hann_window(hann_window_len, device=samples.device)
                hann_window_left, hann_window_right = (
                    hann_window[: hann_window_len // 2],
                    hann_window[hann_window_len // 2 :],
                )

                fading_out, fading_in = (
                    sample[:, start : start + random_lengths[j] // 2],
                    sample[:, start + random_lengths[j] // 2 : start + random_lengths[j]],
                )
                crossfade = hann_window_right * fading_out + hann_window_left * fading_in
                sample = torch.cat(
                    (
                        sample[:, :start],
                        crossfade[:, :],
                        sample[:, start + random_lengths[j] :],
                    ),
                    dim=-1,
                )

            padding = torch.zeros(
                (samples[i].shape[0], samples[i].shape[-1] - sample.shape[-1]),
                dtype=torch.float32,
                device=sample.device,
            )
            sample = torch.cat((sample, padding), dim=-1)
            spliceout_samples.append(sample.unsqueeze(0))

        return ObjectDict(
            samples=torch.cat(spliceout_samples, dim=0),
            sample_rate=sample_rate,
            targets=targets,
            target_rate=target_rate,
        )


class Delay(BaseWaveformTransform):
    def __init__(self, min_shift, max_shift, p=0.5, mode='per_example'):
        super().__init__()
        self.p = p
        self.shift = Shift(min_shift=min_shift, max_shift=max_shift, p=1., mode=mode)

    def apply_transform(self, samples, **kwargs):
        if np.random.random() < self.p:
            shifted_samples = self.shift(samples)
            samples = (samples + shifted_samples) / 2

        return ObjectDict(
            samples=samples,
            **kwargs
        )


class RandAugment:
    def __init__(
            self, 
            sr: int, 
            max_transforms: int = 4, 
            magnitude: int = 7, 
            p: float = 0.5,
            return_params: bool = False,
            mutual_exclusions: bool = True
    ):
        self.return_params = return_params
        self.sr = sr
        self.p = p
        self.max_transforms = max_transforms
        self.magnitude = magnitude
        self.transforms = [
            lambda mag: PolarityInversion(mode='per_example', p=p),
            lambda mag: TimeInversion(mode='per_example', p=p),
            lambda mag: AddColoredNoise(mode='per_example', p=p, min_snr_in_db=5-mag, max_snr_in_db=50-mag),
            lambda mag: Gain(min_gain_in_db=-6.0-mag, max_gain_in_db=0.0, mode='per_example', p=p),
            lambda mag: HighPassFilter(min_cutoff_freq=20+mag*200, max_cutoff_freq=2400+mag*200, mode='per_example', p=p),
            lambda mag: LowPassFilter(min_cutoff_freq=3500-mag*300, max_cutoff_freq=7500-mag*300, mode='per_example', p=p),
            lambda mag: Delay(0.03, 0.06+mag*0.01, p=p),
            lambda mag: PitchShift(-mag, mag, mode='per_example', sample_rate=self.sr, p=p),
            lambda mag: Shift(-.2-mag*0.02, .2+mag*0.02, mode='per_example', p=p),
            # lambda mag: SpliceOut(num_time_intervals=4, max_width=100+mag*10, mode='per_example', p=p),
        ]

        # indices of augmentations where only one at most should get applied
        self.mutual_exclusions = [
            (4, 5),
            # (8, 9)
        ] if mutual_exclusions else []

        self.transform_to_n_params = {
            PolarityInversion : 0,
            TimeInversion : 0,
            AddColoredNoise : 1,
            Gain : 1,
            HighPassFilter : 1,
            LowPassFilter : 1,
            Delay : 1,
            PitchShift : 1,
            Shift : 1,
            SpliceOut : 1
        }

    def __call__(self, x):
        # log original shape, potentially unsqueeze to (B, C, n_samples) 
        # and then reshape to original shape at the end
        original_shape = x.shape
        x = self._ensure_shape(x)
        batch_size = x.shape[0]

        # Sample a subset of indices from the range of transforms and sort them
        sampled_indices = self._sample_augmentations()

        # Select the transforms based on the sampled and sorted indices
        chosen_transforms = [self.transforms[i] for i in sampled_indices]

        # apply transforms
        applied_transforms = {} # (str : actual class) pairs
        for f in chosen_transforms:
            transform = f(self.magnitude)
            x = transform(x, sample_rate=self.sr)
            applied_transforms[self._get_str(transform)] = transform

        transformed = x.view(*original_shape)

        if not self.return_params:
            return transformed
        
        # collect transform parameters
        transform_params = []
        for f in self.transforms:
            # boolean values: was this transform applied?
            f = f(self.magnitude)
            transform_str = self._get_str(f)
            indices = torch.zeros(batch_size)
            if transform_str in applied_transforms:
                transform = applied_transforms[transform_str]
                indices = transform.transform_parameters['should_apply']
                
            transform_params.append(indices.unsqueeze(0))

            # actual settings, for some transforms. start by assuming
            # transform was not one that was applied
            n_params = self.transform_to_n_params[type(f)]
            params = torch.zeros(n_params, batch_size)

            # if we performed this augmentation, get the actual parameters
            if transform_str in applied_transforms:
                try:
                    # then the previous exact same if statement already initialized transform
                    indices = transform.transform_parameters['should_apply'].unsqueeze(0)
                    values = self._get_values_from_transform(transform)

                    if n_params != 0:
                        params[indices] = values
                except:
                    pass
                    
            transform_params.append(params)

        transform_params = torch.cat(transform_params, dim=0).mT

        return transformed, torch.FloatTensor(transform_params)
    
    def _get_str(self, transform):
        return str(type(transform))
    
    def _sample_augmentations(self):
        all_indices = set(range(len(self.transforms)))
        sampled_indices = set()

        # Handle mutually exclusive augmentations
        for group in self.mutual_exclusions:
            if random.random() < self.p:  # Decide whether to apply an augmentation from this group
                sampled_indices.add(random.choice(group))
                all_indices -= set(group)  # Remove all indices from this group

        # Sample remaining augmentations from non-exclusive ones
        num_transforms = random.randint(1, self.max_transforms - len(sampled_indices))
        sampled_indices.update(random.sample(all_indices, min(num_transforms, len(all_indices))))

        return sorted(sampled_indices)
    
    def _get_values_from_transform(self, transform):
        # NOTE: all the unsqueezing is to be future-proof, in case we introduce
        # a new transform that we want to store multiple parameters for.
        if isinstance(transform, AddColoredNoise):
            values = transform.transform_parameters['snr_in_db'].unsqueeze(0)
        elif isinstance(transform, Gain):
            values = transform.transform_parameters['gain_factors'].squeeze().unsqueeze(0)
        elif isinstance(transform, HighPassFilter):
            values = transform.transform_parameters['cutoff_freq'].unsqueeze(0)
        elif isinstance(transform, LowPassFilter):
            values = transform.transform_parameters['cutoff_freq'].unsqueeze(0)
        elif isinstance(transform, Delay):
            values = transform.shift.transform_parameters['num_samples_to_shift'] / self.sr
        elif isinstance(transform, PitchShift):
            values = transform.transform_parameters['transpositions']
            values = torch.tensor([float(v) for v in values]).unsqueeze(0)
        elif isinstance(transform, Shift):
            values = transform.transform_parameters['num_samples_to_shift'] / self.sr
        elif isinstance(transform, SpliceOut):
            values = transform.transform_parameters['splice_lengths']
        else:
            # values doesn't matter
            values = None

        return values

    def _ensure_shape(self, x):
        if x.dim() == 1:
            x = x.unsqueeze(0)
        if x.dim() == 2:
            x = x.unsqueeze(0)
        if x.dim() != 3:
            raise ValueError(f'Invalid shape for RandAugment signal: {x.shape}')

        return x
    
    @property
    def n_params(self):
        return (
            len(self.transforms) - 
            len(self.mutual_exclusions) + 
            sum(v for v in self.transform_to_n_params.values())
        )