""" API processing BM files
"""
from flask import Flask
from flask_cors import CORS
from apis import api
from config import HOST
from sql import db
import os


if os.getenv('LOCAL'):
    database_uri = 'sqlite:////data/hw_bm.db'
else:
    assert os.getenv('MYSQL_USER') and os.getenv('MYSQL_PW') and os.getenv('MYSQL_URL') and os.getenv('MYSQL_DB'), "missing env variables"
    database_uri = 'mysql://'+os.getenv('MYSQL_USER')+':'+os.getenv('MYSQL_PW')+'@'+os.getenv('MYSQL_URL')+'/'+os.getenv('MYSQL_DB')



app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
db.app = app
db.create_all()
api.init_app(app)

CRED = '\033[4;35m'
CEND = '\033[0m'

if __name__ == '__main__':
    if os.getenv('LOCAL'):
        print(CRED + '\nrunning in local mode, data is saved to and read from /data\n' + CEND)
    else:
        print(CRED + '\nrunning in online mode\n' + CEND)

    app.run(debug=True, host=HOST)
