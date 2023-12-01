from dataclasses import dataclass
from typing import Any
from typing import Optional

from sonusai.mixture.datatypes import AudioT


@dataclass(frozen=True)
class Data:
    audio: AudioT
    whisper_model: Optional[Any] = None
    whisper_model_name: Optional[str] = None
    device: Optional[str] = None
