""" API processing BM files
"""
from flask import Flask
from flask_cors import CORS
from apis import api
from config import HOST


app = Flask(__name__)
CORS(app)
api.init_app(app)


if __name__ == '__main__':
    app.run(debug=True, host=HOST)
