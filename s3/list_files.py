"""Handling communication to s3 in order to retrieve files"""
import logging
from math import floor
from operator import attrgetter
import json
import subprocess
import boto3
from botocore.exceptions import ClientError


def list_files(page):
    """Lists all files and returns the amout. WIP definitily needs to be moved to a mysql-db

    Args:
        page (int): page to be displayed

    Returns:
        dict: all summarys
    """

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('hwbenchmark')

    page = 0 if page is None else page

    try:
        # for file in my_bucket.objects.filter():
        files = sorted(
            bucket.objects.filter(Prefix='summary/'),
            key=attrgetter('last_modified'))
        ret_files = files[page * 25:(page + 1) * 25 if (page + 1) * 25 < len(files) else len(files)]
        temp = [{
            'body': json.loads(obj.get()['Body'].read().decode()),
            'last_modified': obj.get()['LastModified'].isoformat(),
            'uuid': str(obj.key).replace('summary/', '').replace('.json', '')
            } for obj in ret_files]
        ret = {
            'data': temp,
            'meta': {
                'page': page,
                'last_page': floor(
                    len(files) /
                    25),
                'total': len(files)}}
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
