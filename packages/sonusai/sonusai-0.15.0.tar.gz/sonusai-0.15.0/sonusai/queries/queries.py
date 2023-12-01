from typing import Any
from typing import Callable

from sonusai.mixture.datatypes import GeneralizedIDs
from sonusai.mixture.mixdb import MixtureDatabase


def get_mixids_from_mixture_field_predicate(mixdb: MixtureDatabase,
                                            field: str,
                                            mixids: GeneralizedIDs = None,
                                            predicate: Callable[[Any], bool] = None) -> dict[int, list[int]]:
    """
    Generate mixture IDs based on mixture field and predicate
    Return a dictionary where:
        - keys are the matching field values
        - values are lists of the mixids that match the criteria
    """
    from typing import Any

    mixid_out = mixdb.mixids_to_list(mixids)

    if predicate is None:
        def predicate(_: Any) -> bool:
            return True

    criteria_set = set()
    for m_id in mixid_out:
        value = getattr(mixdb.mixture(m_id), field)
        if isinstance(value, list):
            for v in value:
                if predicate(v):
                    criteria_set.add(v)
        elif predicate(value):
            criteria_set.add(value)
    criteria = sorted(list(criteria_set))

    result: dict[int, list[int]] = {}
    for criterion in criteria:
        result[criterion] = []
        for m_id in mixid_out:
            value = getattr(mixdb.mixture(m_id), field)
            if isinstance(value, list):
                for v in value:
                    if v == criterion:
                        result[criterion].append(m_id)
            elif value == criterion:
                result[criterion].append(m_id)

    return result


def get_mixids_from_truth_settings_field_predicate(mixdb: MixtureDatabase,
                                                   field: str,
                                                   mixids: GeneralizedIDs = None,
                                                   predicate: Callable[[Any], bool] = None) -> dict[int, list[int]]:
    """
    Generate mixture IDs based on target truth_settings field and predicate
    Return a dictionary where:
        - keys are the matching field values
        - values are lists of the mixids that match the criteria
    """
    from typing import Any

    mixid_out = mixdb.mixids_to_list(mixids)

    # Get all field values
    values = get_all_truth_settings_values_from_field(mixdb, field)

    if predicate is None:
        def predicate(_: Any) -> bool:
            return True

    # Get only values of interest
    values = [value for value in values if predicate(value)]

    result = {}
    for value in values:
        # Get a list of targets for each field value
        indices = []
        for t_id in mixdb.target_file_ids:
            target = mixdb.target_file(t_id)
            for truth_setting in target.truth_settings:
                if value in getattr(truth_setting, field):
                    indices.append(t_id)
        indices = sorted(list(set(indices)))

        mixids = []
        for index in indices:
            for m_id in mixid_out:
                if index in [target.file_id for target in mixdb.mixture(m_id).targets]:
                    mixids.append(m_id)

        mixids = sorted(list(set(mixids)))
        if mixids:
            result[value] = mixids

    return result


def get_all_truth_settings_values_from_field(mixdb: MixtureDatabase, field: str) -> list:
    """
    Generate a list of all values corresponding to the given field in truth_settings
    """
    result = []
    for target in mixdb.target_files:
        for truth_setting in target.truth_settings:
            value = getattr(truth_setting, field)
            if isinstance(value, str):
                value = [value]
            result.extend(value)

    return sorted(list(set(result)))


def get_mixids_from_noise(mixdb: MixtureDatabase,
                          mixids: GeneralizedIDs = None,
                          predicate: Callable[[Any], bool] = None) -> dict[int, list[int]]:
    """
    Generate mixids based on noise index predicate
    Return a dictionary where:
        - keys are the noise indices
        - values are lists of the mixids that match the noise index
    """
    return get_mixids_from_mixture_field_predicate(mixdb=mixdb,
                                                   mixids=mixids,
                                                   field='noise_id',
                                                   predicate=predicate)


def get_mixids_from_target(mixdb: MixtureDatabase,
                           mixids: GeneralizedIDs = None,
                           predicate: Callable[[Any], bool] = None) -> dict[int, list[int]]:
    """
    Generate mixids based on a target index predicate
    Return a dictionary where:
        - keys are the target indices
        - values are lists of the mixids that match the target index
    """
    return get_mixids_from_mixture_field_predicate(mixdb=mixdb,
                                                   mixids=mixids,
                                                   field='target_id',
                                                   predicate=predicate)


def get_mixids_from_snr(mixdb: MixtureDatabase,
                        mixids: GeneralizedIDs = None,
                        predicate: Callable[[Any], bool] = None) -> dict[float, list[int]]:
    """
    Generate mixids based on an SNR predicate
    Return a dictionary where:
        - keys are the SNRs
        - values are lists of the mixids that match the SNR
    """
    from typing import Any

    mixid_out = mixdb.mixids_to_list(mixids)

    # Get all the SNRs
    snrs = [float(snr) for snr in mixdb.all_snrs if not snr.is_random]

    if predicate is None:
        def predicate(_: Any) -> bool:
            return True

    # Get only the SNRs of interest (filter on predicate)
    snrs = [snr for snr in snrs if predicate(snr)]

    result = {}
    for snr in snrs:
        # Get a list of mixids for each SNR
        result[snr] = sorted(
            [i for i, mixture in enumerate(mixdb.mixtures) if mixture.snr == snr and i in mixid_out])

    return result


def get_mixids_from_truth_index(mixdb: MixtureDatabase,
                                mixids: GeneralizedIDs = None,
                                predicate: Callable[[Any], bool] = None) -> dict[int, list[int]]:
    """
    Generate mixids based on a truth index predicate
    Return a dictionary where:
        - keys are the truth indices
        - values are lists of the mixids that match the truth index
    """
    return get_mixids_from_truth_settings_field_predicate(mixdb=mixdb,
                                                          mixids=mixids,
                                                          field='index',
                                                          predicate=predicate)


def get_mixids_from_truth_function(mixdb: MixtureDatabase,
                                   mixids: GeneralizedIDs = None,
                                   predicate: Callable[[Any], bool] = None) -> dict[int, list[int]]:
    """
    Generate mixids based on a truth function predicate
    Return a dictionary where:
        - keys are the truth functions
        - values are lists of the mixids that match the truth function
    """
    return get_mixids_from_truth_settings_field_predicate(mixdb=mixdb,
                                                          mixids=mixids,
                                                          field='function',
                                                          predicate=predicate)
