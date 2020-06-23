"""Handling communication to s3 in order to retrieve files"""
import logging
from math import ceil
import os
import json
import subprocess
import boto3
from botocore.exceptions import ClientError
from sql.summary import Summary
from logic.calculate_score import score


def list_files(page=None):
    """Lists all files and returns the amout.

    Args:
        page (int): page to be displayed

    Returns:
        dict: 25 summarys of the files
    """

    page = 0 if page is None else int(page)

    try:
        # for file in my_bucket.objects.filter():
        per_page = 25

        query = Summary.query
        total_results = query.count()
        query = query.order_by(Summary.created)
        query = query.limit(per_page).offset(per_page * (page - 1))
        results_on_page = query.count()
        data = []
        for res in query:
            summary = json.loads(res.summary)
            temp = {
                'body': {
                    'meta': {
                        'bot_type': res.bot_type,
                        'release': res.release,
                        'battery_type': res.battery_type,
                        'target': res.target

                    },
                    'summary': summary,
                    'overall': score(summary)
                },
                'uuid': res.uuid,
                'last_modified': res.created.isoformat()
            }
            data.append(temp)

        ret = {
            'data': data,
            'meta': {
                'page': page,
                'last_page': ceil(
                    total_results /
                    25),
                'total': total_results,
                'results_on_this_page': results_on_page}
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
        file_path = '/data/' + filename
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except BaseException:
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
