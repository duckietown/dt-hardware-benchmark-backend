"""caslculates the BM_score of all metrics"""
from .config.config import averages


WEIGHT_STD = 0.5


def calc_single(meas, data):
    """calculates the score for one subject

    Args:
        meas (array): dict containting keys and resp. weights
        data (dict): bm data containing the average, e.g. the summary from the DB

    Returns:
        [float]: score
    """
    weights = 0
    average = 0
    rel_std = 0
    for element in meas:
        bm_key = element['name']
        weight = element['weight']
        _format = element['format']

        if data[bm_key]['weighted_avg']:
            weights += weight
            avg = _format(data[bm_key]['weighted_avg']) * weight
            average += min(100, max(0, avg))
            rel_std += data[bm_key]['std'] / data[bm_key]['avg'] * \
                weight if data[bm_key]['avg'] != 0 else data[bm_key]['std'] * weight

    average /= weights
    rel_std /= weights
    total = average - WEIGHT_STD * rel_std
    return min(100, max(0, total))


def calc_container(meas, data):
    """calculates the score for all containers

    Args:
        meas (array): dict containting keys and resp. weights of the containers
        data (dict): bm data containing the average, e.g. the summary from the DB

    Returns:
        [float]: score
    """
    weights = 0
    average = 0
    rel_std = 0

    for element in meas:
        bm_key = element['name']
        weight = element['weight']
        _format = element['format']

        for key, _ in data.items():
            if bm_key in key:
                weights += weight
                avg = _format(data[key]['weighted_avg']) * \
                    weight if data[key]['weighted_avg'] is not None else 0
                average += min(100, max(0, avg))
                if data[key]['avg'] != 0 and data[key]['avg'] and data[key]['std']:
                    rel_std += data[key]['std'] / data[key]['avg'] * weight
                elif data[key]['std'] is not None:
                    rel_std += data[key]['std'] * weight
                else:
                    rel_std += 0

    average /= weights
    rel_std /= weights
    total = average - WEIGHT_STD * rel_std
    return min(100, max(0, total))


def score(data):
    """Calculates overall score

    Args:
        data (dict): summary from DB

    Returns:
        [dict]: score including total.
    """
    score_res = []
    total = 0
    calc_container(averages['Container'], data)
    for key, item in averages.items():
        res = calc_single(
            item,
            data) if key != 'Container' else calc_container(
                item,
                data)
        res = round(res, 2)
        total += res
        score_res.append({'score': res, 'name': key})

    score_res.append(
        {'score': round(total / len(score_res), 2), 'name': 'Total'})
    return score_res
