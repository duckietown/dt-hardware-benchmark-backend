import uuid
import json
import pyrosbag as prb

def process_files_request(request):
    id = uuid.uuid1()
    diagnostics_json_req = json.loads(request['diagnostics_json'])
    meta_json_req = json.loads(request['meta_json'])
    sd_card_json_req = json.loads(request['sd_card_json'])
    bot_bag_req = json.loads(request['bot_bag'])
    meta_req = json.loads(request['meta'])

    with open("temp", "wr") as bag:
        bag.write(bot_bag_req)

    