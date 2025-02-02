from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()
api = Api(version="1.0", title="Asset Management API", description="API for managing tick data and orders")

def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    api.init_app(app)

    # Register namespaces
    from app.api.ticks import ticks_ns
    from app.api.orders import orders_ns
    api.add_namespace(ticks_ns)
    api.add_namespace(orders_ns)

    return app