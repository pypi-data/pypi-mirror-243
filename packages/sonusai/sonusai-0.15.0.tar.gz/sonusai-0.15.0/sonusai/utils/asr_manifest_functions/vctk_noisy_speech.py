from sonusai.utils.asr_manifest_functions import PathInfo
from sonusai.utils.asr_manifest_functions import TranscriptData


def collect_vctk_noisy_speech_transcripts(paths: list[str] | str) -> TranscriptData:
    from glob import iglob
    from os import listdir
    from os.path import abspath
    from os.path import basename
    from os.path import join
    from os.path import split
    from os.path import splitext

    from sonusai import SonusAIError

    entries: TranscriptData = {}
    if not isinstance(paths, list):
        paths = [paths]

    for p in paths:
        abs_p = abspath(p)
        head, tail = split(abs_p)

        dirs = listdir(head)
        tail = tail.replace('wav', 'txt')

        location = None
        for d in dirs:
            if tail.endswith(d):
                location = join(head, d, '*.txt')
                break
        if location is None:
            raise SonusAIError(f'Could not find VCTK Noisy Speech transcript data for {p}')

        for file in iglob(pathname=location, recursive=True):
            with open(file, encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) != 1:
                    raise SonusAIError(f'Ill-formed VCTK Noisy Speech transcript file: {file}')

                name = join(abs_p, splitext(basename(file))[0])
                text = lines[0].lower().strip()

                if name in entries:
                    raise SonusAIError(f'{name} already exists in transcript data')
                entries[name] = text.lower().strip()

    return entries


def get_vctk_noisy_speech_manifest_entry(entry: PathInfo, transcript_data: TranscriptData) -> dict:
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
