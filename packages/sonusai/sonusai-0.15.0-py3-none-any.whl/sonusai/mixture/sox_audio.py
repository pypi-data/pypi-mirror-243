from sox import Transformer as SoxTransformer

from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import ImpulseResponseData


def read_sox_ir(name: str) -> ImpulseResponseData:
    """Read impulse response data using SoX

    :param name: File name
    :return: ImpulseResponseData object
    """
    import numpy as np
    from scipy.io import wavfile

    from sonusai import SonusAIError
    from .tokenized_shell_vars import tokenized_expand
    from .datatypes import ImpulseResponseData

    expanded_name, _ = tokenized_expand(name)

    # Read impulse response data from audio file
    try:
        sample_rate, data = wavfile.read(expanded_name)
    except Exception as e:
        if name != expanded_name:
            raise SonusAIError(f'Error reading {name} (expanded: {expanded_name}): {e}')
        else:
            raise SonusAIError(f'Error reading {name}: {e}')

    data = data.astype(np.float32)
    offset = np.argmax(data)
    data = data[offset:]
    data = data / np.linalg.norm(data)

    return ImpulseResponseData(name=name, sample_rate=sample_rate, data=data)


def read_sox_audio(name: str) -> AudioT:
    """Read audio data from a file using SoX

    :param name: File name
    :return: Array of time domain audio data
    """
    from typing import Any

    import numpy as np
    from sox.core import sox

    from sonusai import SonusAIError
    from .constants import BIT_DEPTH
    from .constants import CHANNEL_COUNT
    from .constants import ENCODING
    from .constants import SAMPLE_RATE
    from .tokenized_shell_vars import tokenized_expand

    def encode_output(buffer: Any) -> np.ndarray:
        from sonusai import SonusAIError
        from .constants import BIT_DEPTH
        from .constants import ENCODING

        if BIT_DEPTH == 8:
            return np.frombuffer(buffer, dtype=np.int8)

        if BIT_DEPTH == 16:
            return np.frombuffer(buffer, dtype=np.int16)

        if BIT_DEPTH == 24:
            return np.frombuffer(buffer, dtype=np.int32)

        if BIT_DEPTH == 32:
            if ENCODING == 'floating-point':
                return np.frombuffer(buffer, dtype=np.float32)
            return np.frombuffer(buffer, dtype=np.int32)

        if BIT_DEPTH == 64:
            return np.frombuffer(buffer, dtype=np.float64)

        raise SonusAIError(f'Invalid BIT_DEPTH {BIT_DEPTH}')

    expanded_name, _ = tokenized_expand(name)

    try:
        # Read in and convert to desired format
        # NOTE: pysox format transformations do not handle encoding properly; need to use direct call to sox instead
        args = [
            '-D',
            '-G',
            expanded_name,
            '-t', 'raw',
            '-r', str(SAMPLE_RATE),
            '-b', str(BIT_DEPTH),
            '-c', str(CHANNEL_COUNT),
            '-e', ENCODING,
            '-',
            'remix', '1',
        ]
        status, out, err = sox(args, None, False)
        if status != 0:
            raise SonusAIError(f'sox stdout: {out}\nsox stderr: {err}')

        return encode_output(out)

    except Exception as e:
        if name != expanded_name:
            raise SonusAIError(f'Error reading {name} (expanded: {expanded_name}):\n{e}')
        else:
            raise SonusAIError(f'Error reading {name}:\n{e}')


class Transformer(SoxTransformer):
    """Override certain sox.Transformer methods
    """

    def fir(self, coefficients):
        """Use SoX’s FFT convolution engine with given FIR filter coefficients.

        The SonusAI override allows coefficients to be either a list of numbers
        or a string containing a text file with the coefficients.

        Parameters
        ----------
        coefficients : list or str
            fir filter coefficients

        """
        from sox.core import is_number

        from sonusai import SonusAIError

        if not isinstance(coefficients, list) and not isinstance(coefficients, str):
            raise SonusAIError("coefficients must be a list or a str.")

        if isinstance(coefficients, list) and not all([is_number(c) for c in coefficients]):
            raise SonusAIError("coefficients list must be numbers.")

        effect_args = ['fir']
        if isinstance(coefficients, list):
            effect_args.extend(['{:f}'.format(c) for c in coefficients])
        else:
            effect_args.append(coefficients)

        self.effects.extend(effect_args)
        self.effects_log.append('fir')

        return self

    def tempo(self, factor, audio_type=None, quick=False):
        """Time stretch audio without changing pitch.

        This effect uses the WSOLA algorithm. The audio is chopped up into
        segments which are then shifted in the time domain and overlapped
        (cross-faded) at points where their waveforms are most similar as
        determined by measurement of least squares.

        The SonusAI override does not generate a warning for small factors.
        The sox.Transformer's implementation of stretch does not invert
        the factor even though it says that it does; this invalidates the
        factor size check and produces the wrong result.

        Parameters
        ----------
        factor : float
            The ratio of new tempo to the old tempo.
            For ex. 1.1 speeds up the tempo by 10%; 0.9 slows it down by 10%.
        audio_type : str
            Type of audio, which optimizes algorithm parameters. One of:
             * m : Music,
             * s : Speech,
             * l : Linear (useful when factor is close to 1),
        quick : bool, default=False
            If True, this effect will run faster but with lower sound quality.

        See Also
        --------
        stretch, speed, pitch

        """
        from sox.core import is_number
        from sox.log import logger

        from sonusai import SonusAIError

        if not is_number(factor) or factor <= 0:
            raise SonusAIError('factor must be a positive number')

        if factor < 0.5 or factor > 2:
            logger.warning('Using an extreme time stretching factor. Quality of results will be poor')

        if audio_type not in [None, 'm', 's', 'l']:
            raise SonusAIError("audio_type must be one of None, 'm', 's', or 'l'.")

        if not isinstance(quick, bool):
            raise SonusAIError('quick must be a boolean')

        effect_args = ['tempo']

        if quick:
            effect_args.append('-q')

        if audio_type is not None:
            effect_args.append('-{}'.format(audio_type))

        effect_args.append('{:f}'.format(factor))

        self.effects.extend(effect_args)
        self.effects_log.append('tempo')

        return self

    def build_array(self, input_filepath=None, input_array=None,
                    sample_rate_in=None, extra_args=None):
        """Given an input file or array, returns the output as a numpy array
        by executing the current set of commands. By default, the array will
        have the same sample rate as the input file unless otherwise specified
        using set_output_format. Functions such as channels and convert
        will be ignored!

        The SonusAI override does not generate a warning for rate transforms.

        Parameters
        ----------
        input_filepath : str or None
            Either path to input audio file or None.
        input_array : np.ndarray or None
            A np.ndarray of a waveform with shape (n_samples, n_channels).
            If this argument is passed, sample_rate_in must also be provided.
            If None, input_filepath must be specified.
        sample_rate_in : int
            Sample rate of input_array.
            This argument is ignored if input_array is None.
        extra_args : list or None, default=None
            If a list is given, these additional arguments are passed to SoX
            at the end of the list of effects.
            Don't use this argument unless you know exactly what you're doing!

        Returns
        -------
        output_array : np.ndarray
            Output audio as a numpy array

        Examples
        --------

        > import numpy as np
        > import sox
        > tfm = sox.Transformer()
        > sample_rate = 44100
        > y = np.sin(2 * np.pi * 440.0 * np.arange(sample_rate * 1.0) / sample_rate)

        file in, array out

        > output_array = tfm.build(input_filepath='path/to/input.wav')

        array in, array out

        > output_array = tfm.build(input_array=y, sample_rate_in=sample_rate)

        specifying the output sample rate

        > tfm.set_output_format(rate=8000)
        > output_array = tfm.build(input_array=y, sample_rate_in=sample_rate)

        if an effect changes the number of channels, you must explicitly
        specify the number of output channels

        > tfm.remix(remix_dictionary={1: [1], 2: [1], 3: [1]})
        > tfm.set_output_format(channels=3)
        > output_array = tfm.build(input_array=y, sample_rate_in=sample_rate)


        """
        import numpy as np
        from sox.core import SoxError
        from sox.core import sox
        from sox.log import logger
        from sox.transform import ENCODINGS_MAPPING

        input_format, input_filepath = self._parse_inputs(
            input_filepath, input_array, sample_rate_in
        )

        # check if any of the below commands are part of the effects chain
        ignored_commands = ['channels', 'convert']
        if set(ignored_commands) & set(self.effects_log):
            logger.warning(
                "When outputting to an array, channels and convert " +
                "effects may be ignored. Use set_output_format() to " +
                "specify output formats."
            )

        output_filepath = '-'

        if input_format.get('file_type') is None:
            encoding_out = np.int16
        else:
            encoding_out = [
                k for k, v in ENCODINGS_MAPPING.items()
                if input_format['file_type'] == v
            ][0]

        n_bits = np.dtype(encoding_out).itemsize * 8

        output_format = {
            'file_type':       'raw',
            'rate':            sample_rate_in,
            'bits':            n_bits,
            'channels':        input_format['channels'],
            'encoding':        None,
            'comments':        None,
            'append_comments': True,
        }

        if self.output_format.get('rate') is not None:
            output_format['rate'] = self.output_format['rate']

        if self.output_format.get('channels') is not None:
            output_format['channels'] = self.output_format['channels']

        if self.output_format.get('bits') is not None:
            n_bits = self.output_format['bits']
            output_format['bits'] = n_bits

        match n_bits:
            case 8:
                encoding_out = np.int8
            case 16:
                encoding_out = np.int16
            case 32:
                encoding_out = np.float32
            case 64:
                encoding_out = np.float64
            case _:
                raise ValueError("invalid n_bits {}".format(n_bits))

        args = []
        args.extend(self.globals)
        args.extend(self._input_format_args(input_format))
        args.append(input_filepath)
        args.extend(self._output_format_args(output_format))
        args.append(output_filepath)
        args.extend(self.effects)

        if extra_args is not None:
            if not isinstance(extra_args, list):
                raise ValueError("extra_args must be a list.")
            args.extend(extra_args)

        status, out, err = sox(args, input_array, False)
        if status != 0:
            raise SoxError(
                "Stdout: {}\nStderr: {}".format(out, err)
            )

        out = np.frombuffer(out, dtype=encoding_out)
        if output_format['channels'] > 1:
            out = out.reshape(
                (
                    output_format['channels'],
                    int(len(out) / output_format['channels'])
                ), order='F'
            ).T
        logger.info(
            "Created array with effects: %s",
            " ".join(self.effects_log)
        )

        return out
