from dataclasses import dataclass

TranscriptData = dict[str, str]


@dataclass(frozen=True)
class PathInfo:
    abs_path: str
    audio_filepath: str
