from flask import Blueprint
from flask_restx import Api
from app.api.orders import orders_ns
from app.api.ticks import ticks_ns

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint, title="True beacon backend", version="1.0", description="tb assignment API operations")

# Add namespaces
api.add_namespace(orders_ns)
api.add_namespace(ticks_ns)
