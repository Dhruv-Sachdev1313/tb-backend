from flask_restx import Namespace, Resource, fields
from flask import request
from app.models.ticks import TickerMaster
from uuid import uuid4

orders_ns = Namespace("orders", description="Order operations")

# Request and response models
order_model = orders_ns.model("Order", {
    "ticker": fields.String(required=True),
    "price": fields.Float(required=True),
    "quantity": fields.Integer(required=True)
})

order_response_model = orders_ns.model("OrderResponse", {
    "message": fields.String(required=True),
    "order_id": fields.Integer(required=True)
})

@orders_ns.route("/place-order")
class PlaceOrder(Resource):
    @orders_ns.doc("place_order")
    @orders_ns.expect(order_model)
    @orders_ns.response(201, "Order placed successfully", order_response_model)
    @orders_ns.response(404, "Ticker not found", orders_ns.model("Error", {"message": fields.String(required=True)}))
    def post(self):
        """Place a mock trade order"""
        data = request.json
        price = data["price"]
        quantity = data["quantity"]
        if price <= 0 or quantity <= 0:
            return {"message": "Price and quantity must be positive"}, 400
        ticker = TickerMaster.query.filter_by(ticker=data["ticker"]).first()
        if not ticker:
            return {"message": "Ticker not found"}, 404
        
        # Simulate order placement
        order_id = uuid4()
        return {"message": "Order placed successfully", "order_id": str(order_id)}, 201