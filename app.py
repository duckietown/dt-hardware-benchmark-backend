from flask import Flask
from apis import api
from flask_cors import CORS
import config


app = Flask(__name__)
CORS(app)
api.init_app(app)


if __name__ == '__main__':
	app.run(debug=True)
