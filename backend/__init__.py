from flask import Flask
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
    app.config["BASE_DIR"] = BASE_DIR
    app.config["UPLOADS_DIR"] = UPLOADS_DIR

    # Register routes
    from routes import init_app as init_routes

    init_routes(app)

    return app
