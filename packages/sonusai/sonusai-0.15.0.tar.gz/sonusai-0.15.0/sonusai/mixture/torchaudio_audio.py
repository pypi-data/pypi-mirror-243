from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import ImpulseResponseData


def read_torchaudio_ir(name: str) -> ImpulseResponseData:
    """Read impulse response data using torchaudio

    :param name: File name
    :return: ImpulseResponseData object
    """
    import numpy as np
    import torch
    import torchaudio

    from sonusai import SonusAIError
    from .tokenized_shell_vars import tokenized_expand
    from .datatypes import ImpulseResponseData

    expanded_name, _ = tokenized_expand(name)

    # Read impulse response data from audio file
    try:
        raw, sample_rate = torchaudio.load(expanded_name, backend='soundfile')
    except Exception as e:
        if name != expanded_name:
            raise SonusAIError(f'Error reading {name} (expanded: {expanded_name}): {e}')
        else:
            raise SonusAIError(f'Error reading {name}: {e}')

    raw = torch.squeeze(raw[0, :])
    offset = torch.argmax(raw)
    raw = raw[offset:]
    # Inexplicably, torch.linalg.vector_norm() causes multiprocessing contexts to hang.
    # Use np.linalg.norm() instead.
    # raw = raw / torch.linalg.vector_norm(raw)

    data = np.array(raw).astype(np.float32)
    data = data / np.linalg.norm(data)

    return ImpulseResponseData(name=name, sample_rate=sample_rate, data=data)


def read_torchaudio_audio(name: str) -> AudioT:
    """Read audio data from a file using torchaudio

    :param name: File name
    :return: Array of time domain audio data
    """
    import numpy as np
    import torch
    import torchaudio

    from sonusai import SonusAIError
    from .constants import SAMPLE_RATE
    from .tokenized_shell_vars import tokenized_expand

    expanded_name, _ = tokenized_expand(name)

    try:
        out, samplerate = torchaudio.load(expanded_name, backend='soundfile')
        out = torch.reshape(out[0, :], (1, out.size()[1]))

        if not samplerate == SAMPLE_RATE:
            out = torchaudio.functional.resample(out, orig_freq=samplerate, new_freq=SAMPLE_RATE)
    except Exception as e:
        if name != expanded_name:
            raise SonusAIError(f'Error reading {name} (expanded: {expanded_name}):\n{e}')
        else:
            raise SonusAIError(f'Error reading {name}:\n{e}')

    result = np.squeeze(np.array(out))
    return result
