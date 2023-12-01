from sonusai.utils.asr_manifest_functions import PathInfo
from sonusai.utils.asr_manifest_functions import TranscriptData


def collect_librispeech_transcripts(paths: list[str] | str) -> TranscriptData:
    from glob import iglob
    from os.path import abspath
    from os.path import dirname
    from os.path import join

    from sonusai import SonusAIError

    entries: TranscriptData = {}
    if not isinstance(paths, list):
        paths = [paths]

    for p in paths:
        location = join(abspath(p), '**', '*.trans.txt')
        for file in iglob(pathname=location, recursive=True):
            root = dirname(file)
            with open(file, encoding='utf-8') as f:
                for line in f:
                    name, text = line[: line.index(' ')], line[line.index(' ') + 1:]
                    name = join(root, name)
                    if name in entries:
                        raise SonusAIError(f'{name} already exists in transcript data')
                    entries[name] = text.lower().strip()
    return entries


def get_librispeech_manifest_entry(entry: PathInfo, transcript_data: TranscriptData) -> dict:
    from os.path import splitext
    from subprocess import check_output

    from sonusai import SonusAIError

    name = splitext(entry.abs_path)[0]
    duration = float(check_output(f'soxi -D {entry.abs_path}', shell=True))
    if name not in transcript_data.keys():
        raise SonusAIError(f'Could not find {name} in transcript data')

    return {
        'audio_filepath': entry.audio_filepath,
        'text':           transcript_data[name],
        'duration':       duration,
    }
