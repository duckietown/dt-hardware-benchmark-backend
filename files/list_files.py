"""Handling communication to s3 in order to retrieve files"""
import logging
from math import ceil
from operator import attrgetter
import json
import subprocess
import boto3
from botocore.exceptions import ClientError
from sql.summary import Summary
import random
import os

from logic.calculate_score import score 


def list_files(page=None):
    """Lists all files and returns the amout. WIP: summary definitily needs to be moved to a mysql-db

    Args:
        page (int): page to be displayed

    Returns:
        dict: 25 summarys of the files
    """

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('hwbenchmark')

    page = 0 if page is None else int(page)

    try:
        # for file in my_bucket.objects.filter():
        perPage = 25

        query = Summary.query
        totalResults = query.count()
        query = query.order_by(Summary.created)
        query = query.limit(perPage).offset(perPage*(page-1))
        resultsOnPage = query.count()
        
        data = []

        for res in query:
            temp = {
                'body': {
                    'meta': {
                        'bot_type': res.bot_type,
                        'release': res.release,
                        'battery_type': res.battery_type,
                        'target': res.target

                    },
                    'summary': res.summary,
                    'overall': score(json.loads(res.summary))
                },
                'uuid':  res.uuid,
                'last_modified': res.created.isoformat()
            }
            data.append(temp)

        ret = {
            'data': data,
            'meta': {
                'page': page,
                'last_page': ceil(
                    totalResults /
                    25),
                'total': totalResults,
                'results_on_this_page': resultsOnPage}
                }
        return ret

    except ClientError as exc:
        logging.error(exc)
        return False
    return True


def get_file(filename):
    """ Used to get a specific file from s3

    Args:
        filename ([uuid]): uuid of searched file

    Returns:
        file content as dict
    """

    # Upload the file


    if os.getenv('LOCAL'):
        file_path = '/data/'+filename
        try:
            with open(file_path, 'r') as file:
                res = file.read()
                return res
        except:
            return False
    else:        
        s3 = boto3.resource('s3')

        try:
            # for file in my_bucket.objects.filter():
            temp_fn = 'temp_' + filename.split('/')[-1]
            s3.meta.client.download_file('hwbenchmark', filename, temp_fn)
            with open(temp_fn, 'r') as file:
                ret = json.load(file)
            subprocess.Popen(["rm", temp_fn])
            return ret

        except ClientError as exc:
            logging.error(exc)
            return False
    return True
