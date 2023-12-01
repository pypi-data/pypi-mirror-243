"""mkmanifest

usage: mkmanifest [-hvn] [--include GLOB] [-m METHOD] [-e ADAT] [-o OUTPUT] PATH ...

options:
    -h, --help
    -v, --verbose                   Be verbose: list all files found.
    -n, --dry-run                   Collect files, but exit without processing and writing manifest file.
    --include GLOB                  Search only files whose base name matches GLOB. [default: *.{wav,flac}].
    -m METHOD, --method METHOD      Method for getting the true speech text of the audio files. [default: librispeech].
    -e ADAT, --audio-env ADAT       Environment variable pointing to all audio data.
    -o OUTPUT, --output OUTPUT      Output file name. [default: asr_manifest.json].

Make a speech recognition (ASR) .json manifest file of all audio files under PATHS following the NVIDIA NeMo format.
An example of manifest entries:

{"audio_filepath": "<absolute_path_to>/1355-39947-0000.wav", "duration": 11.3, "text": "psychotherapy ..."}
{"audio_filepath": "<absolute_path_to>/1355-39947-0001.wav", "duration": 15.905, "text": "it is an ..."}

See the NVIDIA NeMo docs for more information:
https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/asr/datasets.html

Inputs:
    PATH        A relative path name or list of paths containing audio files. Each will be
                recursively searched for files matching the pattern GLOB.
    GLOB        Match the pattern GLOB using wildcard matching.
                Example: '*.{wav,flac}' matches all .wav and .flac files.
    METHOD      The method to use for fetching the true speech of the audio files.
                Supported methods:
                    - 'librispeech'
                    - 'vctk_noisy_speech'
    ADAT        Audio data environment variable. All found files will be expanded to their full, absolute path and
                then parts of the path that match the specified environment variable value will be replaced with
                the variable. This accommodates portability across platforms where the sound datasets may in
                different locations.
    OUTPUT      Name of output file. Default is asr_manifest.json.

Outputs the following to the current directory:
    <OUTPUT>
    mkmanifest.log

Example usage for LibriSpeech:
  sonusai mkmanifest -mlibrispeech -eADAT -oasr_manifest.json --include='*.flac' train-clean-100

"""
from sonusai import logger

VALID_METHOD = ['librispeech', 'vctk_noisy_speech']


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    dry_run = args['--dry-run']
    include = args['--include']
    method = args['--method']
    audio_env = args['--audio-env']
    output = args['--output']
    paths = args['PATH']

    import json
    from functools import partial
    import time
    from os import environ
    from os.path import abspath
    from os.path import join
    from os.path import realpath

    from tqdm import tqdm

    from sonusai import SonusAIError
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.utils import braced_iglob
    from sonusai.utils import pp_tqdm_imap
    from sonusai.utils import seconds_to_hms
    from sonusai.utils.asr_manifest_functions import PathInfo
    from sonusai.utils.asr_manifest_functions import collect_librispeech_transcripts
    from sonusai.utils.asr_manifest_functions import collect_vctk_noisy_speech_transcripts
    from sonusai.utils.asr_manifest_functions import get_librispeech_manifest_entry
    from sonusai.utils.asr_manifest_functions import get_vctk_noisy_speech_manifest_entry

    start_time = time.monotonic()

    create_file_handler('mkmanifest.log')
    update_console_handler(verbose)
    initial_log_messages('mkmanifest')

    if method not in VALID_METHOD:
        raise SonusAIError(f'Unknown method: {method}')

    audio_dir = None
    if audio_env is not None:
        audio_dir = realpath(environ[audio_env])
        if audio_dir is None:
            raise SonusAIError(f'Unknown environment variable: {audio_env}')

    if audio_env:
        for p in paths:
            if not realpath(abspath(p)).startswith(audio_dir):
                logger.warning(f'Specified directory, {p}, is not part of the provided audio environment: '
                               f'${audio_env}={audio_dir}')

    logger.info('')
    logger.info(f'Searching {len(paths)} provided director{"ies" if len(paths) > 1 else "y"}...')

    entries: list[PathInfo] = []
    for p in paths:
        location = join(realpath(abspath(p)), '**', include)
        logger.debug(f'Processing {location}')
        for file in braced_iglob(pathname=location, recursive=True):
            name = file
            if audio_env is not None:
                name = name.replace(audio_dir, f'${audio_env}')
            entries.append(PathInfo(abs_path=file, audio_filepath=name))
        logger.debug('')

    logger.info(f'Found {len(entries)} audio file{"s" if len(entries) != 1 else ""}')

    if dry_run:
        logger.info('')
        logger.info('Dry run')
        logger.info('')
        for entry in entries:
            logger.info(f' - {entry.audio_filepath}')
        return

    if method == 'librispeech':
        logger.info('Collecting LibriSpeech transcript data')
        transcript_data = collect_librispeech_transcripts(paths=paths)

        processing_func = partial(get_librispeech_manifest_entry, transcript_data=transcript_data)
        progress = tqdm(total=len(entries), desc='Creating LibriSpeech manifest data')
        results = pp_tqdm_imap(processing_func, entries, progress=progress)
        progress.close()

        with open(output, 'w') as f:
            for result in results:
                f.write(json.dumps(result) + '\n')

    if method == 'vctk_noisy_speech':
        logger.info('Collecting VCTK Noisy Speech transcript data')
        transcript_data = collect_vctk_noisy_speech_transcripts(paths=paths)

        processing_func = partial(get_vctk_noisy_speech_manifest_entry, transcript_data=transcript_data)
        progress = tqdm(total=len(entries), desc='Creating VCTK Noisy Speech manifest data')
        results = pp_tqdm_imap(processing_func, entries, progress=progress)
        progress.close()

        with open(output, 'w') as f:
            for result in results:
                f.write(json.dumps(result) + '\n')

    end_time = time.monotonic()
    logger.info('')
    logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')
    logger.info('')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
