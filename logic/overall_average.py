"""Claculating the overall average for alll Benchmarks TODO:definiteley needs to be cached"""
import logging
from math import ceil
import os
from operator import attrgetter
import json
import subprocess
import boto3
from botocore.exceptions import ClientError
from sql.summary import Summary

from logic.calculate_score import score 


def calc_overall_average():
    """Calculates the overall average

    Returns:
        dict: complete summary overa all submitted data
    """

    query = Summary.query
    query = query.filter_by(accepted=True)
    totalResults = query.count()
    
    data = []
    first = True
    for res in query:
        sc = score(json.loads(res.summary))
        if first:
            data = sc
            first = False
        else:
            for i, elem in enumerate(sc):
                data[i]['score'] += elem['score']

    for i in range(len(data)):
        data[i]['score'] /= totalResults
        data[i]['score'] = round(data[i]['score'], 2)
    
    return data

