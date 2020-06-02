from dotenv import load_dotenv
import enum

load_dotenv(verbose=True)

BATTERY_TYPES = [ 'older/foreign', 'Old Alu', 'New Intelligent' ]

BOT_TYPES = [ 'older', 'DB17', 'DB18p1', 'DB18p2', 'DB18p3', 'DB18p4', 'DB19', 'DB20', 'DB21/DBv2' ]

RELEASES = [ 'older/other', 'master19', 'daffy' ] #, 'ente' ]