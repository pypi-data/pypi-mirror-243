from multiprocessing import current_process
from multiprocessing import get_context
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Optional

from tqdm import tqdm

CONTEXT = 'fork'


def pp_tqdm_imap(func: Callable,
                 *iterables: Iterable,
                 initializer: Optional[Callable[..., None]] = None,
                 initargs: Optional[Iterable[Any]] = None,
                 progress: Optional[tqdm] = None,
                 num_cpus: Optional[int] = None,
                 total: Optional[int] = None,
                 no_par: bool = False) -> list[Any]:
    """Performs a parallel ordered imap with tqdm progress."""
    from os import cpu_count
    from typing import Sized

    if total is None:
        total = min(len(iterable) for iterable in iterables if isinstance(iterable, Sized))

    results: list[Any] = [None] * total
    n = 0
    if no_par or current_process().daemon:
        if initializer is not None:
            if initargs is not None:
                initializer(*initargs)
            else:
                initializer()

        for result in map(func, *iterables):
            results[n] = result
            n += 1
            if progress is not None:
                progress.update()
    else:
        if num_cpus is None:
            num_cpus = cpu_count()
        elif num_cpus is float:
            num_cpus = int(round(num_cpus * cpu_count()))

        if total < num_cpus:
            num_cpus = total
        with get_context(CONTEXT).Pool(processes=num_cpus, initializer=initializer, initargs=initargs) as pool:
            for result in pool.imap(func, *iterables):  # type: ignore
                results[n] = result
                n += 1
                if progress is not None:
                    progress.update()
            pool.close()
            pool.join()

    if progress is not None:
        progress.close()
    return results


pp_imap = pp_tqdm_imap
