"""Module formatting the data in order to save, calculates the std, mneand, etc"""
from functools import reduce
import operator
import copy
import numpy as np
from scipy import interpolate


def retrieve_from_extern(data, keys, format_, t0, calc=None, no_time=False):
    """ helper function retrieving one measurement,
            doing formatting and calculating
    """
    k = keys[0]
    res = []
    time = []

    if no_time:
        time = np.arange(1, len(data), 1)
    for i, meas in enumerate(data[k]):
        formatted = float(meas if not format_ else format_(meas))
        sol = [calc(formatted)] if calc else [formatted]
        res.append(sol[0])
        if not no_time:
            time.append(data['time'][i] - t0)
    return time, res


def retrieve_from_keys(data, group, keys, format_, calc=None):
    """ helper function retrieving one measurement,
            doing formatting and calculating
    """
    res = np.zeros(len(data[group]))
    for i, meas in enumerate(data[group]):
        local_res = []
        for key in keys:
            reduced = reduce(operator.getitem, key.split('.'), meas)
            local_res.append(
                float(
                    reduced if not format_ else format_(reduced)))
        sol = [calc(*local_res)] if calc else local_res
        res[i] = sol[0]
    return res


def retrieve_from_containers(
        data,
        group,
        container_id,
        keys,
        format_,
        t0,
        calc=None):
    """ helper function retrieving one measurement,
            doing formatting and calculating
    """
    res = []
    time = []

    for meas in data[group]:
        if meas['container'] == container_id:
            local_res = []
            for key in keys:
                reduced = reduce(operator.getitem, key.split('.'), meas)
                local_res.append(
                    float(
                        reduced if not format_ else format_(reduced)))
            sol = [calc(*local_res)] if calc else local_res

            t = meas['time'] - t0
            if t in time:
                i = time.index(t)
                res[i] += sol[0]
            else:
                res.append(sol[0])
                time.append(meas['time'] - t0)
    return time, res


def process_data(res, t, t_meas, y, synthetic_t0=False):
    """ Function that generates all used measurements in order to be saved as one bm measurement"""
    res = copy.deepcopy(res)

    if len(t_meas) > 1:
        if not res.get('ip'):
            # set up cubic spline interpolation
            c_spline = interpolate.CubicSpline(t_meas, y)
            y_ip = np.round(c_spline(t), decimals=2)
        else:
            interp = res['ip'](t_meas, y)
            y_ip = np.round(interp(t), decimals=2)
    else:
        y_ip = y * len(t)

    res_multi = res.get('avg_multiplier', 1)

    weighted_avg = 0
    try:
        if not res.get('avg_weigh_lower', False):
            weighted_avg = weighted_average_focus_high(
                np.array(y) * res_multi) / res_multi
        else:
            weighted_avg = weighted_average_focus_low(
                np.array(y) * res_multi) / res_multi
    except BaseException:
        weighted_avg = None

    if np.isnan(weighted_avg):
        weighted_avg = None

    res['t'] = t_meas
    res['measurement'] = y
    res['measurement_ip'] = y_ip
    res['info'] = res.get('info') if res.get('info') else ""
    res['info'] += "!! time not synced !!" if synthetic_t0 else ""
    if y is not None and len(y) > 0:
        res['min'] = np.min(y)
        res['max'] = np.max(y)
        res['mean'] = np.mean(y, dtype=np.float64)
        res['weighted_avg'] = weighted_avg
        res['median'] = np.median(y)
        res['std'] = np.std(y, dtype=np.float64)

    return res


def collect_data(data, meas, t):
    """ returns meas-dict extended with measurements from the data (json)
            interpolates between the data,
            as well as doing statisical analysis
    """
    search_key = list(meas.keys())
    try:
        search_key.remove('container')
        search_key.remove('process')
    except ValueError:
        pass

    t0 = data['general']['time']
    for group_key, group_items in meas.items():
        if group_key != 'containers_cfg':
            for index, item in enumerate(group_items):
                if group_key == 'extern':
                    t_meas, y = retrieve_from_extern(item.get('data'), item.get('keys'), item.get(
                        'format'), t0 if not item.get('t0') else item.get('t0'),
                                                     item.get('calc'), item.get('notime', False))
                else:
                    t_meas = retrieve_from_keys(
                        data, group_key, ['time'], lambda t: t - t0)
                    y = retrieve_from_keys(data, group_key, item.get(
                        'keys'), item.get('format'), item.get('calc'))
                meas[group_key][index] = process_data(
                    meas[group_key][index], t, t_meas, y, item.get('t0'))

    # collecting data fdrom all containers or processes
    meas['containers'] = []
    for cont_cfg in meas['containers_cfg']:
        base_key = str(cont_cfg.get('keys').split('.')[0])
        data_key = str(cont_cfg.get('keys').split('.')[1])
        for cont_id, cont in data['containers'].items():
            res = copy.deepcopy(cont_cfg)
            res['name'] = cont + res.get('base_name')
            res['export_name'] = cont + '_' + data_key
            t_meas, y = retrieve_from_containers(copy.deepcopy(data), base_key, cont_id, [data_key],
                                                 res.get('format'), t0 if not res.get('t0') else
                                                 res.get('t0'), res.get('calc'))
            res = process_data(res, t, t_meas, y, res.get('t0'))
            meas['containers'].append(res)

    del meas['containers_cfg']
    return meas

# {"bot_type":"DB18p4","battery_type":"Old Alu","release":"master19"}


def weight_function(x):
    """Weight function punishing the upper outliers 10 more than lower

    Args:
        x (np.array): array of which the weighing function is claculated,
                      uses values between 0 and 100

    Returns:
        np.array: weight per entry
    """
    a = 7.91E-4
    b = 1.732
    return np.exp(a * (np.array(x)**b))


def weighted_average_focus_high(x):
    """Calculates weighted average"""
    weights = weight_function(x)
    total_weight = np.sum(weights)
    total = np.sum(weights * x)
    if total == 0:
        return 0
    return total / total_weight


def weighted_average_focus_low(x):
    """Calculates weighted average"""
    weights = weight_function(-x + 100 * np.ones(len(x)))
    total_weight = np.sum(weights)
    total = np.sum(weights * x)
    if total == 0:
        return 0
    return total / total_weight


def collect_meta(data, meta_dict, meta_data, bot_type, battery_type, release):
    """collect metadata"""
    res = meta_data
    res['bot_type'] = bot_type
    res['battery_type'] = battery_type
    res['release'] = release
    for key, item in meta_dict.items():
        res[key] = reduce(operator.getitem, item.split('.'), data)
    return res
