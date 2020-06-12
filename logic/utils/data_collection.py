from functools import reduce
import operator
import json
import base64
import numpy as np
from scipy import interpolate


def retrieve_from_extern(data, keys, format, t0, calc=None):
    """ helper function retrieving one measurement,
            doing formatting and calculating
    """
    k = keys[0]
    res = []
    time = []
    for i, meas in enumerate(data[k]):
        formatted = float(meas if not format else format(meas))
        sol = [calc(formatted)] if calc else [formatted]
        res.append(sol[0])
        time.append(data['time'][i] - t0)
    return time, res


def retrieve_from_keys(data, group, keys, format, calc=None):
    """ helper function retrieving one measurement,
            doing formatting and calculating
    """
    print("line 26" + group)
    res = np.zeros(len(data[group]))
    for i, meas in enumerate(data[group]):
        local_res = []
        for key in keys:
            print(key.split('.'))
            reduced = reduce(operator.getitem, key.split('.'), meas)
            local_res.append(float(reduced if not format else format(reduced)))
        sol = [calc(*local_res)] if calc else local_res
        res[i] = sol[0]
    return res


def retrieve_from_containers(
        data,
        group,
        container,
        keys,
        format,
        t0,
        calc=None):
    """ helper function retrieving one measurement,
            doing formatting and calculating
    """
    res = []
    time = []
    container_id = ''

    for key, cont in data['containers'].items():
        if (cont == container):
            container_id = key
            break

    key = 'process_stats' if group == 'process' else 'container_stats'

    for meas in data[key]:
        if (meas['container'] == container_id):
            local_res = []
            for key in keys:
                reduced = reduce(operator.getitem, key.split('.'), meas)
                local_res.append(
                    float(
                        reduced if not format else format(reduced)))
            sol = [calc(*local_res)] if calc else local_res

            t = meas['time'] - t0
            if t in time:
                i = time.index(t)
                res[i] += sol[0]
            else:
                res.append(sol[0])
                time.append(meas['time'] - t0)
    return time, res


def collect_data(data, meas, t):
    """ returns meas-dict extended with measurements from the data (json)
            interpolates between the data,
            as well as doing statisical analysis
    """
    search_key = list(meas.keys())
    try:
        search_key.remove('container')
        search_key.remove('process')
    except BaseException:
        pass

    with open("testrr.json", "w+") as file:
        file.write(json.dumps(data))

    t0 = data['general']['time']
    for group_key, group_items in meas.items():
        for index, item in enumerate(group_items):
            if (group_key == 'container' or group_key == 'process'):
                converted_keys = list(
                    map(lambda x: x.split('.', 1)[1], item.get('keys')))
                t_meas, y = retrieve_from_containers(data,
                                                     group_key,
                                                     item.get('keys')[0].split('.', 1)[0],
                                                     converted_keys,
                                                     item.get('format'),
                                                     t0 if not item.get('t0') else item.get('t0'),
                                                     item.get('calc'))
            elif group_key == 'extern':
                t_meas, y = retrieve_from_extern(item.get('data'), item.get('keys'), item.get(
                    'format'), t0 if not item.get('t0') else item.get('t0'), item.get('calc'))
            else:
                t_meas = retrieve_from_keys(
                    data, group_key, ['time'], lambda t: t - t0)
                y = retrieve_from_keys(data, group_key, item.get('keys'),
                                       item.get('format'), item.get('calc'))

            if len(t_meas) > 1:
                if not meas[group_key][index].get('ip'):
                    cs = interpolate.CubicSpline(
                        t_meas, y)  # set up cubic spline interpolation
                    y_ip = np.round(cs(t), decimals=2)
                else:
                    ip = meas[group_key][index]['ip'](t_meas, y)
                    y_ip = np.round(ip(t), decimals=2)
            else:
                y_ip = y * len(t)

            print(group_key, index, item, y)
            meas[group_key][index]['t'] = t_meas
            meas[group_key][index]['measurement'] = y
            meas[group_key][index]['measurement_ip'] = y_ip
            meas[group_key][index]['info'] = meas[group_key][index].get(
                'info') if meas[group_key][index].get('info') else ""
            meas[group_key][index]['info'] += "!! time not synced !!" if item.get(
                't0') else ""
            if y is not None and len(y) > 0:
                meas[group_key][index]['min'] = np.min(y)
                meas[group_key][index]['max'] = np.max(y)
                meas[group_key][index]['mean'] = np.mean(y, dtype=np.float64)
                meas[group_key][index]['weighted_avg'] = weighted_average_focus_high(
                    y)
                meas[group_key][index]['median'] = np.median(y)
                meas[group_key][index]['std'] = np.std(y, dtype=np.float64)
    return meas


def weight_function(x):
    a = 7.91E-4
    b = 1.732
    return np.exp(a * np.array(x)**b)


def weighted_average_focus_high(x):
    total_weight = np.sum(weight_function(x))
    total = np.sum(weight_function(x) * x)
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
