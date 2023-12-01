from functools import lru_cache

from pyaaware import ForwardTransform
from pyaaware import InverseTransform

from sonusai.mixture.datatypes import AudioF
from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import EnergyT
from sonusai.mixture.datatypes import ImpulseResponseData


def get_next_noise(audio: AudioT, offset: int, length: int) -> AudioT:
    """Get next sequence of noise data from noise audio file

    :param audio: Overall noise audio (entire file's worth of data)
    :param offset: Starting sample
    :param length: Number of samples to get
    :return: Sequence of noise audio data
    """
    import numpy as np

    return np.take(audio, range(offset, offset + length), mode='wrap')


def calculate_transform_from_audio(audio: AudioT,
                                   transform: ForwardTransform) -> tuple[AudioF, EnergyT]:
    """Apply forward transform to input audio data to generate transform data

    :param audio: Time domain data [samples]
    :param transform: ForwardTransform object
    :return: Frequency domain data [frames, bins], Energy [frames]
    """
    f, e = transform.execute_all(audio)
    return f.transpose(), e


def calculate_audio_from_transform(data: AudioF,
                                   transform: InverseTransform,
                                   trim: bool = True) -> tuple[AudioT, EnergyT]:
    """Apply inverse transform to input transform data to generate audio data

    :param data: Frequency domain data [frames, bins]
    :param transform: InverseTransform object
    :param trim: Removes starting samples so output waveform will be time-aligned with input waveform to the transform
    :return: Time domain data [samples], Energy [frames]
    """
    t, e = transform.execute_all(data.transpose())
    if trim:
        t = t[transform.N - transform.R:]

    return t, e


def get_duration(audio: AudioT) -> float:
    """Get duration of audio in seconds

    :param audio: Time domain data [samples]
    :return: Duration of audio in seconds
    """
    from .constants import SAMPLE_RATE

    return len(audio) / SAMPLE_RATE


def validate_input_file(input_filepath: str) -> None:
    from os.path import exists
    from os.path import splitext

    from soundfile import available_formats

    from sonusai import SonusAIError

    if not exists(input_filepath):
        raise SonusAIError(f'input_filepath {input_filepath} does not exist.')

    ext = splitext(input_filepath)[1][1:].lower()
    read_formats = [item.lower() for item in available_formats().keys()]
    if ext not in read_formats:
        raise SonusAIError(f'This installation of SoX cannot process .{ext} files')


@lru_cache
def read_audio(name: str) -> AudioT:
    """Read audio data from a file

    :param name: File name
    :return: Array of time domain audio data
    """
    from .torchaudio_audio import read_torchaudio_audio

    return read_torchaudio_audio(name)


@lru_cache
def read_ir(name: str) -> ImpulseResponseData:
    """Read impulse response data

    :param name: File name
    :return: ImpulseResponseData object
    """
    from .torchaudio_audio import read_torchaudio_ir

    return read_torchaudio_ir(name)
