from flask import Flask
from api_v_1.bootstrap import api
import os

app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api/v1")


if __name__ == '__main__':
    app.run()