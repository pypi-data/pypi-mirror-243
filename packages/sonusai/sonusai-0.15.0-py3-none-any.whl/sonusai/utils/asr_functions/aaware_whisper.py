from sonusai.utils import ASRResult
from sonusai.utils.asr_functions.data import Data


def aaware_whisper(data: Data) -> ASRResult:
    import tempfile
    from math import exp
    from os import getenv
    from os.path import join

    import requests

    from sonusai import SonusAIError
    from sonusai.utils import ASRResult
    from sonusai.utils import float_to_int16
    from sonusai.utils import write_wav

    url = getenv('AAWARE_WHISPER_URL')
    if url is None:
        raise SonusAIError(f'AAWARE_WHISPER_URL environment variable does not exist')
    url += '/asr?task=transcribe&language=en&encode=true&output=json'

    with tempfile.TemporaryDirectory() as tmp:
        file = join(tmp, 'asr.wav')
        write_wav(name=file, audio=float_to_int16(data.audio))

        files = {'audio_file': (file, open(file, 'rb'), 'audio/wav')}

        try:
            response = requests.post(url, files=files)
            if not response.status_code == 200:
                if response.status_code == 422:
                    raise SonusAIError(f'Validation error: {response.json()}')
                raise SonusAIError(f'Invalid response: {response.status_code}')
            result = response.json()
            return ASRResult(text=result['text'], confidence=exp(float(result['segments'][0]['avg_logprob'])))
        except Exception as e:
            raise SonusAIError(f'Aaware Whisper exception: {e.args}')


"""
Aaware Whisper Asr Webservice results:
{
  "text": " The birch canoes slid on the smooth planks.",
  "segments": [
    {
      "id": 0,
      "seek": 0,
      "start": 0.0,
      "end": 2.32,
      "text": " The birch canoes slid on the smooth planks.",
      "tokens": [
        50364, 440, 1904, 339, 393, 78, 279, 1061, 327, 322, 264, 5508, 499,
        14592, 13, 50480
      ],
      "temperature": 0.0,
      "avg_logprob": -0.385713913861443,
      "compression_ratio": 0.86,
      "no_speech_prob": 0.006166956853121519
    }
  ],
  "language": "en"
}
"""
