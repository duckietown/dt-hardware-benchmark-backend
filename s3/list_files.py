import logging
import boto3
from math import floor
from botocore.exceptions import ClientError
from operator import attrgetter
import json
import subprocess


def list_files(page):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('hwbenchmark')

    page = 0 if page is None else page
    
    try:
        # for file in my_bucket.objects.filter():
        files = sorted(bucket.objects.filter(Prefix='summary/'), key=attrgetter('last_modified'))
        ret_files = files[page*25:(page+1)*25 if (page+1)*25 < len(files) else len(files)]
        temp = [{'body': json.loads(obj.get()['Body'].read().decode()), 
                 'last_modified': obj.get()['LastModified'].isoformat(), 
                 'uuid': str(obj.key).replace('summary/', '').replace('.json', '') } 
                for obj in ret_files]
        ret = {'data':temp, 'meta': {'page': page, 'last_page': floor(len(files)/25), 'total': len(files)}}
        return ret

    except ClientError as e:
        logging.error(e)
        return False
    return True

def get_file(filename):

    # Upload the file
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('hwbenchmark')
    
    try:
        # for file in my_bucket.objects.filter():
        temp_fn = 'temp_'+filename.split('/')[-1]
        s3.meta.client.download_file('hwbenchmark', filename, temp_fn)
        with open(temp_fn, 'r') as file:
            ret = json.load(file)
        subprocess.run(["rm", temp_fn])
        return ret

    except ClientError as e:
        logging.error(e)
        return False
    return True