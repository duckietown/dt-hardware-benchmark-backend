""" Procvesses all bm realted files and saves them to the given loaction, mainly in s3
"""
import uuid
import json
import subprocess

from secrets import APP_SECRET, APP_ID

import numpy as np
import requests

from config import DIAGNOSTICS_DATABASE, DIAGNOSTICS_BASE_URL

from files.upload_file import upload_file, upload_summary
from .utils.analyze_rosbag import run
from .utils.data_collection import collect_data, collect_meta
from .utils.export import export_json, export_summary_json
from .config.master19 import meta, measurements


def storage2json(filestorage, args):
    """turns filestorage to json

    Args:
        filestorage (string): name of file storage in args
        args (parser.args): args of a restplus parser

    Returns:
        dict: dict containing json data
    """
    return json.loads(str(args[filestorage].read().decode('ascii')))


def process_files_request(args, hw_bm_file_key=None):
    """Takes all files from the requiest, performs the benchmark analysis and saves them to s3

    Args:
        args (parser.args): args of resplus parser
        hw_bm_file_key (string, optional): Key to . Defaults to None.
    """

    bm_uuid = uuid.uuid1()

    if hw_bm_file_key is None:
        diagnostics_json_req = storage2json('diagnostics_json', args)
    else:
        # Get Data from diagnostics API
        url = '{}/json?app_id={}&app_secret={}&database={}&key={}'.format(
            DIAGNOSTICS_BASE_URL, APP_ID, APP_SECRET, DIAGNOSTICS_DATABASE, hw_bm_file_key)
        req = requests.get(url)
        diagnostics_json_req = req.json()['data']['value']
        health_url = "{}/seek=health".format(url)
        req_health = requests.get(health_url)
        health_json = req_health.json()['data']['value']

        diagnostics_json_req['health'] = health_json

        with open('test.json', 'w+') as file:
            file.write(json.dumps(diagnostics_json_req))
        with open('test_health.json', 'w+') as file:
            file.write(json.dumps(health_json))

    #read all bm data submitted
    meta_json_req = storage2json('meta_json', args)
    sd_card_json_req = storage2json('sd_card_json', args)
    meta_req = json.loads(args['meta'])
    latencies_bag_req = args['latencies_bag'].read()

    botname = diagnostics_json_req['general']['target']
    bagname = 'temp_%s.bag' % bm_uuid
    filename = '%s.json' % bm_uuid

    try:
        #analyze rosbag
        with open(bagname, 'wb') as bag:
            bag.write(latencies_bag_req)

        segs, lat = run(bagname, botname)

        bm_buffer = 0
        t = np.round(
            np.linspace(
                bm_buffer,
                diagnostics_json_req['general']['duration'] -
                bm_buffer,
                200),
            decimals=2)

        print(meta_req)

        #prepare saving of data.
        collected_meta = collect_meta(
            diagnostics_json_req,
            meta,
            meta_json_req,
            meta_req['bot_type'],
            meta_req['battery_type'],
            meta_req['release'])
        collected_data = collect_data(
            diagnostics_json_req, measurements(
                lat, segs, sd_card_json_req)['diagnostics'], t)
        overall = [{'name': 'CPU', 'score': 100}, {'name': 'Ram', 'score': 20}]

        #upload
        content = export_json(collected_data, collected_meta, t)
        upload_file(content, 'meas/' + filename)
        summary = export_summary_json(collected_data, collected_meta, overall)
        upload_summary(bm_uuid, json.loads(summary))

        if args['localization_bag'] is not None:
            upload_file(
                args['localization_bag'].read(),
                'loc/%s.bag' %
                bm_uuid)

    finally:
        #cleanup
        subprocess.Popen(["rm", bagname])

    return bm_uuid
