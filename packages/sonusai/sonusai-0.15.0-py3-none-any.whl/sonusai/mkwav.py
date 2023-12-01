"""sonusai mkwav

usage: mkwav [-hvtn] [-i MIXID] LOC

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -i MIXID, --mixid MIXID         Mixture ID(s) to generate. [default: *].
    -t, --target                    Write target file.
    -n, --noise                     Write noise file.

The mkwav command creates WAV files from a SonusAI database.

Inputs:
    LOC         A SonusAI mixture database directory.
    MIXID       A glob of mixture ID(s) to generate.

Outputs the following to the mixture database directory:
    <id>_mixture.wav:   mixture
    <id>_target.wav:    target (optional)
    <id>_noise.wav:     noise (optional)
    <id>.txt
    mkwav.log

"""
from dataclasses import dataclass

from sonusai import logger
from sonusai.mixture import AudioT
from sonusai.mixture import MixtureDatabase


@dataclass
class MPGlobal:
    mixdb: MixtureDatabase = None
    write_target: bool = None
    write_noise: bool = None


MP_GLOBAL = MPGlobal()


def mkwav(location: str, mixid: int) -> tuple[AudioT, AudioT, AudioT]:
    import numpy as np

    from sonusai.genmix import genmix

    data = genmix(location=location, mixids=mixid, force=False)

    return data[0].mixture, np.sum(data[0].targets, axis=0), data[0].noise


def _process_mixture(mixid: int) -> None:
    from os.path import exists
    from os.path import join
    from os.path import splitext

    import h5py
    import numpy as np

    from sonusai.mixture import mixture_metadata
    from sonusai.utils import float_to_int16
    from sonusai.utils import write_wav

    mixture_filename = join(MP_GLOBAL.mixdb.location, MP_GLOBAL.mixdb.mixtures[mixid].name)
    mixture_basename = splitext(mixture_filename)[0]

    target = None
    noise = None

    need_data = True
    if exists(mixture_filename + '.h5'):
        with h5py.File(mixture_filename, 'r') as f:
            if 'mixture' in f:
                need_data = False
            if MP_GLOBAL.write_target and 'targets' not in f:
                need_data = True
            if MP_GLOBAL.write_noise and 'noise' not in f:
                need_data = True

    if need_data:
        mixture, target, noise = mkwav(location=MP_GLOBAL.mixdb.location, mixid=mixid)
    else:
        with h5py.File(mixture_filename, 'r') as f:
            mixture = np.array(f['mixture'])
            if MP_GLOBAL.write_target:
                target = np.sum(np.array(f['targets']), axis=0)
            if MP_GLOBAL.write_noise:
                noise = np.array(f['noise'])

    write_wav(name=mixture_basename + '_mixture.wav', audio=float_to_int16(mixture))
    if MP_GLOBAL.write_target:
        write_wav(name=mixture_basename + '_target.wav', audio=float_to_int16(target))
    if MP_GLOBAL.write_noise:
        write_wav(name=mixture_basename + '_noise.wav', audio=float_to_int16(noise))

    with open(file=mixture_basename + '.txt', mode='w') as f:
        f.write(mixture_metadata(MP_GLOBAL.mixdb, MP_GLOBAL.mixdb.mixture(mixid)))


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    mixid = args['--mixid']
    MP_GLOBAL.write_target = args['--target']
    MP_GLOBAL.write_noise = args['--noise']
    location = args['LOC']

    import time
    from os.path import join

    from tqdm import tqdm

    import sonusai
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.mixture import check_audio_files_exist
    from sonusai.utils import pp_tqdm_imap
    from sonusai.utils import human_readable_size
    from sonusai.utils import seconds_to_hms

    start_time = time.monotonic()

    create_file_handler(join(location, 'mkwav.log'))
    update_console_handler(verbose)
    initial_log_messages('mkwav')

    logger.info(f'Load mixture database from {location}')
    MP_GLOBAL.mixdb = MixtureDatabase(location)
    mixid = MP_GLOBAL.mixdb.mixids_to_list(mixid)

    total_samples = MP_GLOBAL.mixdb.total_samples(mixid)
    duration = total_samples / sonusai.mixture.SAMPLE_RATE

    logger.info('')
    logger.info(f'Found {len(mixid):,} mixtures to process')
    logger.info(f'{total_samples:,} samples')

    check_audio_files_exist(MP_GLOBAL.mixdb)

    progress = tqdm(total=len(mixid))
    pp_tqdm_imap(_process_mixture, mixid, progress=progress)
    progress.close()

    logger.info(f'Wrote {len(mixid)} mixtures to {location}')
    logger.info('')
    logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
    logger.info(f'mixture:  {human_readable_size(total_samples * 2, 1)}')
    if MP_GLOBAL.write_target:
        logger.info(f'target:   {human_readable_size(total_samples * 2, 1)}')
    if MP_GLOBAL.write_noise:
        logger.info(f'noise:    {human_readable_size(total_samples * 2, 1)}')

    end_time = time.monotonic()
    logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')
    logger.info('')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
