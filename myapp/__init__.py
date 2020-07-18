from flask import Flask
from api.routes import blueprint
from site.routes import site


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint)
    app.register_blueprint(site)

    return app
