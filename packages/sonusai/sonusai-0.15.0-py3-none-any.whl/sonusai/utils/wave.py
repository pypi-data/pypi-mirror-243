from sonusai.mixture.constants import SAMPLE_RATE
from sonusai.mixture.datatypes import AudioT


def write_wav(name: str, audio: AudioT, sample_rate: int = SAMPLE_RATE) -> None:
    """ Write a simple, uncompressed WAV file.

    To write multiple channels, use a 2D array of shape [samples, channels].
    The bits per sample and PCM/float are determined by the data type.

    """
    import numpy as np
    import torch
    import torchaudio

    if audio.ndim == 1:
        audio = np.reshape(audio, (1, audio.shape[0]))

    torchaudio.save(name, torch.tensor(audio), sample_rate)
