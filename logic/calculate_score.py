from .config.config import averages


WEIGHT_STD = 0.5

def calc_single(meas, data):
    weights = 0
    average = 0
    rel_std = 0
    for element in meas:
        bm_key = element['name']
        weight = element['weight']
        _format = element['format']

        weights += weight
        av = _format(data[bm_key]['weighted_avg']) * weight
        average += min(100, max(0, av))
        rel_std += data[bm_key]['std'] / data[bm_key]['avg'] * weight if data[bm_key]['avg'] != 0 else data[bm_key]['std'] * weight

    average /= weights
    rel_std /= weights
    total = average - WEIGHT_STD * rel_std
    return min(100, max(0, total))

def calc_container(meas, data):
    weights = 0
    average = 0
    rel_std = 0

    for element in meas:
        bm_key = element['name']
        weight = element['weight']
        _format = element['format']

        for key, item in data.items():
            if bm_key in key:
                weights += weight
                av = _format(data[key]['weighted_avg']) * weight if data[key]['weighted_avg'] is not None else 0
                average += min(100, max(0, av))
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
    score_res = []
    total = 0
    calc_container(averages['Container'], data)
    for key, item in averages.items():
        res = calc_single(item, data) if key != 'Container' else calc_container(item, data)
        res = round(res, 2)
        total += res
        score_res.append({'score': res, 'name': key})

    score_res.append({'score': round(total/len(score_res), 2), 'name': 'Total'})
    return score_res