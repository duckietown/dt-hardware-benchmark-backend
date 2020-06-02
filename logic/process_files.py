import uuid
import json
import pyrosbag as prb
from .utils.analyze_rosbag import run
import subprocess

def process_files_request(request):

    id = uuid.uuid1()
    diagnostics_json_req = json.loads(request['diagnostics_json'])
    meta_json_req = json.loads(request['meta_json'])
    sd_card_json_req = json.loads(request['sd_card_json'])
    latencies_bag_req = request['latencies_bag']
    meta_req = request['meta']

    with open("temp.bag", "wt") as bag:
        bag.write(latencies_bag_req)
        subprocess.run(["rm", "temp.orig.bag"])
        subprocess.run(["rosbag", "reindex", "temp.bag"])
    
    run()

    