import uuid
import json
import subprocess
import numpy as np

from s3.upload_file import upload_file
from .utils.analyze_rosbag import run
from .utils.data_collection import collect_data, collect_meta
from .utils.export import export_json, export_summary_json
from .config.master19 import meta, measurements

def storage2json(fs, args):
    return json.loads(str(args[fs].read().decode('ascii')))

def process_files_request(args):
    
    id = uuid.uuid1()

    diagnostics_json_req = storage2json('diagnostics_json', args)
    meta_json_req = storage2json('meta_json', args)
    sd_card_json_req = storage2json('sd_card_json', args)

    meta_req = json.loads(args['meta'])
    latencies_bag_req = args['latencies_bag'].read()

    botname = diagnostics_json_req['general']['target']
    bagname = 'temp_%s.bag' % id
    filename = '%s.json' % id

    try:
        with open(bagname, 'wb') as bag:
            bag.write(latencies_bag_req)
        
        segs, lat = run(bagname, botname)

        bm_buffer = 0
        t = np.round(np.linspace(bm_buffer, diagnostics_json_req['general']['duration'] - bm_buffer, 200), decimals=2)

        collected_meta = collect_meta(diagnostics_json_req, meta, meta_json_req, meta_req['bot_type'], meta_req['battery_type'], meta_req['release'])
        collected_data = collect_data(diagnostics_json_req, measurements(lat, segs, sd_card_json_req)['diagnostics'], t)
        overall = [{'name':'CPU','score': 100}, {'name':'Ram', 'score': 20}]


        content = export_json(collected_data, collected_meta, t)
        upload_file(content, 'meas/'+filename)
        summary = export_summary_json(collected_data, collected_meta, overall)
        upload_file(summary, 'summary/'+filename)

    finally:
        subprocess.run(["rm", bagname])
    