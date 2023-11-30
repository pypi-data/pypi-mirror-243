from flask import Flask

from flask_ujson import UJSON

ultra_json = UJSON()


def create_app():
    app = Flask(__name__)
    ultra_json.init_app(app)

    @app.route("/")
    def index():
        return {"hello": "world"}

    return app
