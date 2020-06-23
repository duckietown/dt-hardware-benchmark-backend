"""Calculating the overall average for alll Benchmarks TODO:definiteley needs to be cached"""
import json
from sql.summary import Summary

from logic.calculate_score import score


def calc_overall_average():
    """Calculates the overall average

    Returns:
        dict: complete summary overa all submitted data
    """

    query = Summary.query
    query = query.filter_by(accepted=True)
    total_results = query.count()

    data = []
    first = True
    for res in query:
        res_score = score(json.loads(res.summary))
        if first:
            data = res_score
            first = False
        else:
            for i, elem in enumerate(res_score):
                data[i]['score'] += elem['score']

    for i, _ in enumerate(data): #in order to prevent weird copyiong errors
        data[i]['score'] /= total_results
        data[i]['score'] = round(data[i]['score'], 2)

    return data
