from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


# Initialize extensions
db = SQLAlchemy()
myapi = Api(version="1.0", title="Asset Management API", description="API for managing tick data and orders")

def create_app(config_class="app.configs.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)
    # Initialize extensions
    db.init_app(app)
    from app.api import api_blueprint
    app.register_blueprint(api_blueprint)

    return app