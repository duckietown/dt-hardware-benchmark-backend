"""Handles Communitation to s3 in order to upload file"""
import logging
import os
import json
import boto3
from botocore.exceptions import ClientError
from sql.summary import Summary
from sql import db


def upload_file(content, file_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :return: True if file was uploaded, else False
    """

    # Upload the file
    if os.getenv('LOCAL'):
        file_path = '/data/' + file_name
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, 'w' if isinstance(content, str) else 'wb') as file:
            file.write(content)
        return True

    s3 = boto3.resource('s3')
    try:
        s3.Object('hwbenchmark', file_name).put(Body=content)
    except ClientError as exc:
        logging.error(exc)
        return False
    return True


def upload_summary(uuid, summary):
    """uploads a summary to a SQL DB

    Args:
        uuid (uuid): uuid of experiment
        summary (dict): summary to be uploaded
    """
    summary = Summary(uuid=str(uuid),
                      bot_type=summary['meta']['bot_type'],
                      battery_type=summary['meta']['battery_type'],
                      release=summary['meta']['release'],
                      target=summary['meta']['target'],
                      summary=json.dumps(summary['summary']),
                      accepted=True)  # hardcoded for the moment TODO
    db.session.add(summary)
    db.session.commit()
