"""Handles Communitation to s3 in order to upload file"""
import logging
import boto3
from botocore.exceptions import ClientError
import os
from shutil import copy2
import datetime
import json
from sql.summary import Summary
from sql import db

def upload_file(content, file_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :return: True if file was uploaded, else False
    """

    # Upload the file
    if os.getenv('LOCAL'):
        file_path = '/data/'+file_name
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, 'w' if type(content) is str else 'wb') as file:
            print(file_name)
            file.write(content)
        
    else:
        s3 = boto3.resource('s3')
        try:
            response = s3.Object('hwbenchmark', file_name).put(Body=content)
            print(response)
        except ClientError as exc:
            logging.error(exc)
            return False
        return True

def upload_summary(uuid, summary):
    s = Summary(uuid=str(uuid), 
                bot_type=summary['meta']['bot_type'],
                battery_type=summary['meta']['battery_type'],
                release=summary['meta']['release'],
                target=summary['meta']['target'],
                overall=json.dumps(summary['overall']),
                summary=json.dumps(summary['summary']))
    db.session.add(s)
    db.session.commit()