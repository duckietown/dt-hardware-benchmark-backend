""" API processing BM files
"""
import os
from flask import Flask
from flask_cors import CORS
from apis import api
from config import HOST
from sql import db

LOCAL_VARIABLES = ['APP_ID', 'APP_SECRET']
ONLINE_VARIABLES = ['APP_ID', 'APP_SECRET', 'MYSQL_USER', 'MYSQL_PW', 'MYSQL_URL', 'MYSQL_DB', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']

CRED = '\033[4;35m'
CEND = '\033[0m'

DATABASE_URI = ''

if os.getenv('LOCAL'):
    for e in LOCAL_VARIABLES:
        assert os.getenv(e),  "missing env variable {}, needed: \n{}".format(e, '\n'.join(LOCAL_VARIABLES)) 
    DATABASE_URI = 'sqlite:////data/hw_bm.db'
    print(
        CRED +
        '\nrunning in local mode, data is saved to and read from /data\n' +
        CEND)
else:
    for e in ONLINE_VARIABLES:
        assert os.getenv(e),  "missing env variable {}, needed: \n{}".format(e, '\n'.join(ONLINE_VARIABLES)) 

    DATABASE_URI = (
        'mysql://' +
        os.getenv('MYSQL_USER') +
        ':' +
        os.getenv('MYSQL_PW') +
        '@' +
        os.getenv('MYSQL_URL') +
        '/' +
        os.getenv('MYSQL_DB'))
    print(CRED + '\nrunning in online mode\n' + CEND)


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
db.app = app
db.create_all()
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host=HOST)
