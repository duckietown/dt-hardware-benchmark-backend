import logging
import boto3
from botocore.exceptions import ClientError


def upload_file(content, file_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3 = boto3.resource('s3')
    try:
        response = s3.Object('hwbenchmark', file_name+'.txt').put(Body=content)
        #response = s3_client.upload_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True