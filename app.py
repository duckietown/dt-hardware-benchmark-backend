""" API processing BM files
"""
import os
from flask import Flask
from flask_cors import CORS
from apis import api
from config import HOST
from sql import db


CRED = '\033[4;35m'
CEND = '\033[0m'

DATABASE_URI = ''
if os.getenv('LOCAL'):
    DATABASE_URI = 'sqlite:////data/hw_bm.db'
    print(
        CRED +
        '\nrunning in local mode, data is saved to and read from /data\n' +
        CEND)
else:
    assert (os.getenv('MYSQL_USER') and os.getenv('MYSQL_PW') and os.getenv(
        'MYSQL_URL') and os.getenv('MYSQL_DB') and os.getenv('AWS_ACCESS_KEY_ID') 
        and os.getenv('AWS_SECRET_ACCESS_KEY')), "missing env variables"
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
