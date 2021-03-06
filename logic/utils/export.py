"""used to export measured data to a file"""
import json
import numpy as np


class NumpyArrayEncoder(json.JSONEncoder):
    """treats turns np.arrays in normal arrays for json export"""

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def export_measurements_json(meas, meta, t):
    """exports measurements as json string"""
    res = {'time': t}
    for _, group_items in meas.items():
        for item in group_items:
            res[item['export_name']] = item['measurement_ip']
    assembled = {'meta': meta, 'data': res}
    return json.dumps(assembled, cls=NumpyArrayEncoder)


def export_json(meas, meta, t):
    """exports complete measurements as json string"""
    res = {'time': t}
    for _, group_items in meas.items():
        for item in group_items:
            current = {}
            for key, value in item.items():
                if not callable(value) and not key == 'data':
                    current[key] = value
            res[item['export_name']] = current
    assembled = {'meta': meta, 'measurements': res}
    return json.dumps(assembled, cls=NumpyArrayEncoder)


def export_summary_json(meas, meta):
    """exports measurements as json string"""
    res = {}
    for _, group_items in meas.items():
        for item in group_items:
            res[item['export_name']] = {'avg': item.get('mean'), 'std': item.get(
                'std'), 'weighted_avg': item.get('weighted_avg')}
    assembled = {'meta': meta, 'summary': res}
    return json.dumps(assembled, cls=NumpyArrayEncoder)
