"""sonusai genmix

usage: genmix [-hvgts] [-i MIXID] LOC

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -i MIXID, --mixid MIXID         Mixture ID(s) to generate. [default: *].
    -g, --target                    Save target. [default: False].
    -t, --truth                     Save truth_t. [default: False].
    -s, --segsnr                    Save segsnr_t. [default: False].

Generate SonusAI mixture data from a SonusAI mixture database.

Inputs:
    LOC         A SonusAI mixture database directory.
    MIXID       A glob of mixture ID(s) to generate.

Outputs the following to the mixture database directory:
    <id>.h5:
        dataset:    mixture
        dataset:    targets
        dataset:    noise
        dataset:    target (optional)
        dataset:    truth_t (optional)
        dataset:    segsnr_t (optional)
    <id>.txt
    genmix.log
"""
from dataclasses import dataclass

from sonusai import logger
from sonusai.mixture import GenMixData
from sonusai.mixture import GeneralizedIDs
from sonusai.mixture import MixtureDatabase


@dataclass
class MPGlobal:
    mixdb: MixtureDatabase = None
    save_target: bool = None
    compute_truth: bool = None
    compute_segsnr: bool = None
    force: bool = None
    write: bool = None


MP_GLOBAL = MPGlobal()


def genmix(location: str,
           mixids: GeneralizedIDs = None,
           save_target: bool = False,
           compute_truth: bool = False,
           compute_segsnr: bool = False,
           write: bool = False,
           show_progress: bool = False,
           force: bool = True) -> list[GenMixData]:
    from tqdm import tqdm

    from sonusai.utils import pp_tqdm_imap

    mixdb = MixtureDatabase(location)
    mixids = mixdb.mixids_to_list(mixids)
    progress = tqdm(total=len(mixids), disable=not show_progress)
    results = pp_tqdm_imap(_genmix_kernel,
                           mixids,
                           initializer=_genmix_initializer,
                           initargs=(location, save_target, compute_truth, compute_segsnr, force, write),
                           progress=progress)
    progress.close()

    return results


def _genmix_initializer(location: str,
                        save_target: bool,
                        compute_truth: bool,
                        compute_segsnr: bool,
                        force: bool,
                        write: bool) -> None:
    MP_GLOBAL.mixdb = MixtureDatabase(location)
    MP_GLOBAL.save_target = save_target
    MP_GLOBAL.compute_truth = compute_truth
    MP_GLOBAL.compute_segsnr = compute_segsnr
    MP_GLOBAL.force = force
    MP_GLOBAL.write = write


def _genmix_kernel(m_id: int) -> GenMixData:
    from sonusai.mixture import write_mixture_data
    from sonusai.mixture import write_mixture_metadata

    mixdb = MP_GLOBAL.mixdb
    save_target = MP_GLOBAL.save_target
    compute_truth = MP_GLOBAL.compute_truth
    compute_segsnr = MP_GLOBAL.compute_segsnr
    force = MP_GLOBAL.force
    write = MP_GLOBAL.write

    targets = mixdb.mixture_targets(m_id=m_id, force=force)
    noise = mixdb.mixture_noise(m_id=m_id, force=force)
    write_data = [('targets', targets), ('noise', noise)]

    if compute_truth:
        truth_t = mixdb.mixture_truth_t(m_id=m_id, targets=targets, noise=noise, force=force)
        write_data.append(('truth_t', truth_t))
    else:
        truth_t = None

    target = mixdb.mixture_target(m_id=m_id, targets=targets)
    if save_target:
        write_data.append(('target', target))

    if compute_segsnr:
        segsnr_t = mixdb.mixture_segsnr_t(m_id=m_id,
                                          targets=targets,
                                          target=target,
                                          noise=noise,
                                          force=force)
        write_data.append(('segsnr_t', segsnr_t))
    else:
        segsnr_t = None

    mixture = mixdb.mixture_mixture(m_id=m_id,
                                    targets=targets,
                                    target=target,
                                    noise=noise,
                                    force=force)
    write_data.append(('mixture', mixture))

    if write:
        write_mixture_data(mixdb, mixdb.mixture(m_id), write_data)
        write_mixture_metadata(mixdb, mixdb.mixture(m_id))

    return GenMixData(targets=targets,
                      noise=noise,
                      mixture=mixture,
                      truth_t=truth_t,
                      segsnr_t=segsnr_t)


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    import time
    from os.path import join

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import check_audio_files_exist
    from sonusai.utils import human_readable_size
    from sonusai.utils import seconds_to_hms

    verbose = args['--verbose']
    location = args['LOC']
    mixids = args['--mixid']
    save_target = args['--target']
    compute_truth = args['--truth']
    compute_segsnr = args['--segsnr']

    start_time = time.monotonic()

    create_file_handler(join(location, 'genmix.log'))
    update_console_handler(verbose)
    initial_log_messages('genmix')

    logger.info(f'Load mixture database from {location}')
    mixdb = MixtureDatabase(location)
    mixids = mixdb.mixids_to_list(mixids)

    total_samples = mixdb.total_samples(mixids)
    duration = total_samples / sonusai.mixture.SAMPLE_RATE

    logger.info('')
    logger.info(f'Found {len(mixids):,} mixtures to process')
    logger.info(f'{total_samples:,} samples')

    check_audio_files_exist(mixdb)

    genmix(location=location,
           mixids=mixids,
           save_target=save_target,
           compute_truth=compute_truth,
           compute_segsnr=compute_segsnr,
           write=True,
           show_progress=True)

    logger.info(f'Wrote {len(mixids)} mixtures to {location}')
    logger.info('')
    logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
    logger.info(f'mixture:  {human_readable_size(total_samples * 2, 1)}')
    if compute_truth:
        logger.info(f'truth_t:  {human_readable_size(total_samples * mixdb.num_classes * 4, 1)}')
    logger.info(f'target:   {human_readable_size(total_samples * 2, 1)}')
    logger.info(f'noise:    {human_readable_size(total_samples * 2, 1)}')
    if compute_segsnr:
        logger.info(f'segsnr:   {human_readable_size(total_samples * 4, 1)}')

    end_time = time.monotonic()
    logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')
    logger.info('')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
