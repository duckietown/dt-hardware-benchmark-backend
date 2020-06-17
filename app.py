""" API processing BM files
"""
from flask import Flask
from flask_cors import CORS
from apis import api
from config import HOST
from sql import db
import os


if os.getenv('LOCAL'):
    databaseUri = 'sqlite:////data/hw_bm.db'
else:
    databaseUri = 'mysql://'+mysqlConfig.user+':'+mysqlConfig.pw+'@'+mysqlConfig.server+'/'+mysqlConfig.database


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = databaseUri
db.init_app(app)
db.app = app
db.create_all()
api.init_app(app)


if __name__ == '__main__':
    if os.getenv('LOCAL'):
        print('running in local version, data is saved to /data')

    app.run(debug=True, host=HOST)
