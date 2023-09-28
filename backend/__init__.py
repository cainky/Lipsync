from flask import Flask
from flask_cors import CORS
from config import Config, DevelopmentConfig, TestingConfig, ProductionConfig


def create_app(config="default"):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    configurations = {
        "default": Config,
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    app.config.from_object(configurations[config])

    # Register routes
    from routes import init_app as init_routes

    init_routes(app)

    return app
