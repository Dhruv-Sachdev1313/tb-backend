from flask_restx import Namespace, Resource, fields

orders_ns = Namespace("orders", description="Order operations")

# Request and response models
order_model = orders_ns.model("Order", {
    "symbol": fields.String(required=True),
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
    @orders_ns.marshal_with(order_response_model)
    def post(self):
        """Place a mock trade order"""
        data = orders_ns.payload
        # Simulate order placement
        order_id = 12345  # Mock order ID
        return {"message": "Order placed successfully", "order_id": order_id}, 201