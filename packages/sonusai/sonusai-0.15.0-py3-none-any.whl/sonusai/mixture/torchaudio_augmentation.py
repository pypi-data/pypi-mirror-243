from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import Augmentation
from sonusai.mixture.datatypes import ImpulseResponseData


def apply_torchaudio_augmentation(audio: AudioT,
                                  augmentation: Augmentation,
                                  length_common_denominator: int = 1) -> AudioT:
    """Apply augmentations to audio data using torchaudio.sox_effects

    :param audio: Audio
    :param augmentation: Augmentation
    :param length_common_denominator: Pad resulting audio to be a multiple of this
    :return: Augmented audio
    """
    import numpy as np
    import torch
    import torchaudio

    from sonusai import SonusAIError
    from .augmentation import _pad_audio
    from .constants import SAMPLE_RATE

    effects: list[list[str]] = []

    # TODO
    #  Always normalize and remove normalize from list of available augmentations
    #  Normalize to globally set level (should this be a global config parameter,
    #  or hard-coded into the script?)
    if augmentation.normalize is not None:
        effects.append(['norm', str(augmentation.normalize)])

    if augmentation.gain is not None:
        effects.append(['gain', str(augmentation.gain)])

    if augmentation.pitch is not None:
        effects.append(['pitch', str(augmentation.pitch)])
        effects.append(['rate', str(SAMPLE_RATE)])

    if augmentation.tempo is not None:
        effects.append(['tempo', '-s', str(augmentation.tempo)])

    if augmentation.eq1 is not None:
        effects.append(['equalizer', *[str(item) for item in augmentation.eq1]])

    if augmentation.eq2 is not None:
        effects.append(['equalizer', *[str(item) for item in augmentation.eq2]])

    if augmentation.eq3 is not None:
        effects.append(['equalizer', *[str(item) for item in augmentation.eq3]])

    if augmentation.lpf is not None:
        effects.append(['lowpass', '-2', str(augmentation.lpf), '0.707'])

    if effects:
        if audio.ndim == 1:
            audio = np.reshape(audio, (1, audio.shape[0]))
        out = torch.tensor(audio)

        try:
            out, _ = torchaudio.sox_effects.apply_effects_tensor(out,
                                                                 sample_rate=SAMPLE_RATE,
                                                                 effects=effects)
        except Exception as e:
            raise SonusAIError(f'Error applying {augmentation}: {e}')

        audio_out = np.squeeze(np.array(out))
    else:
        audio_out = audio

    # make sure length is multiple of length_common_denominator
    return _pad_audio(audio=audio_out, length_common_denominator=length_common_denominator)


def apply_torchaudio_ir(audio: AudioT, ir: ImpulseResponseData) -> AudioT:
    """Apply impulse response to audio data using torchaudio.fftconvolve

    :param audio: Audio
    :param ir: Impulse response data
    :return: Augmented audio
    """
    import numpy as np
    import torch
    import torchaudio

    from sonusai.utils import linear_to_db
    from .constants import SAMPLE_RATE

    # Early exit if no ir or if all audio is zero
    if ir is None or not audio.any():
        return audio

    # Get current maximum level in dB
    max_db = linear_to_db(max(abs(audio)))

    # Convert audio to IR sample rate
    audio_in = torch.reshape(torch.tensor(audio), (1, len(audio)))
    audio_out, sr = torchaudio.sox_effects.apply_effects_tensor(audio_in,
                                                                sample_rate=SAMPLE_RATE,
                                                                effects=[['rate', str(ir.sample_rate)]])

    # Apply IR and convert back to global sample rate
    rir = torch.reshape(torch.tensor(ir.data), (1, len(ir.data)))
    audio_out = torchaudio.functional.fftconvolve(audio_out, rir)
    audio_out, sr = torchaudio.sox_effects.apply_effects_tensor(audio_out,
                                                                sample_rate=ir.sample_rate,
                                                                effects=[['rate', str(SAMPLE_RATE)]])

    # Reset level to previous max value
    audio_out, sr = torchaudio.sox_effects.apply_effects_tensor(audio_out,
                                                                sample_rate=SAMPLE_RATE,
                                                                effects=[['norm', str(max_db)]])

    return np.squeeze(np.array(audio_out[:, :len(audio)]))
