""" Config
"""
from dotenv import load_dotenv

load_dotenv(verbose=True)

HOST = '0.0.0.0'

DIAGNOSTICS_DATABASE = 'db_log_default'
DIAGNOSTICS_BASE_URL = 'https://dashboard.duckietown.org/web-api/1.0/data/get'

BATTERY_TYPES = ['older/foreign', 'Old Alu', 'New Intelligent']
BOT_TYPES = [
    'older',
    'DB17',
    'DB18p1',
    'DB18p2',
    'DB18p3',
    'DB18p4',
    'DB19',
    'DB20',
    'DB21/DBv2']
RELEASES = ['older/other', 'master19', 'daffy']  # , 'ente' ]
