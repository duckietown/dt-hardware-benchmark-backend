import rosbag
import json
import re
import yaml
from rospy_message_converter import message_converter

import os


def stamp2time(stamp):
    return stamp.get('secs') + stamp.get('nsecs')/1000000000.0

def retrieve_latencies(bag, duckiename):
    lat = {'time': [], 'meas': []}

    find_msg_re = r'^(\[LineDetectorNode\] \d+:\sLatencies:\s)'
    find_line_re = r'\s+--pub_lines--\s+\|\s+total\s+latency\s+\d+.\d+ ms\s+'
    
    for _, msg, _ in bag.read_messages(topics=['/rosout']):
        temp = message_converter.convert_ros_message_to_dictionary(msg)
                        
        msg_string = temp.get('msg')
        if temp.get('name') == '/{}/line_detector_node'.format(duckiename) and re.search(find_msg_re, temp.get('msg')):                  
            time = stamp2time(temp.get('header').get('stamp'))
            for line in msg_string.split('\n'):
                if re.search(find_line_re,  line):
                    snippet = re.findall(find_line_re,  line)[0]
                    lat['time'].append(time)
                    lat['meas'].append(re.findall(r'\d+.\d+',snippet)[0])
    return lat


def retrieve_segment_count(bag, duckiename):

    segs = {'time': [], 'meas': []}

    for _, msg, _ in bag.read_messages(topics=['/{}/line_detector_node/segment_list'.format(duckiename)]):
        temp = message_converter.convert_ros_message_to_dictionary(msg)
        time = stamp2time(temp.get('header').get('stamp'))
        
        segs['time'].append(time)
        segs['meas'].append(len(temp.get('segments')))
    return segs

def run(bagname, duckiename, savetoJson=False):

    with rosbag.Bag(bagname, 'r') as bag:
        segs = retrieve_segment_count(bag, duckiename)
        lat = retrieve_latencies(bag, duckiename)

    if savetoJson:    
        with open('{}_latencies.json'.format(bagname), 'w') as file:
            file.write(json.dumps(lat))

        with open('{}_segment_counts.json'.format(bagname), 'w') as file:
            file.write(json.dumps(segs))

    return segs, lat