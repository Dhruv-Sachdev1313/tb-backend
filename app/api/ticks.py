from flask_restx import Namespace, Resource, fields
from app.services.tick_service import get_ticks
from datetime import datetime
from flask import request
from app.models.ticks import TickerMaster

ticks_ns = Namespace("ticks", description="Tick data operations")

# Request and response models
tick_model = ticks_ns.model("Tick", {
    "ts": fields.DateTime(required=True),
    "ticker": fields.String(required=True),
    "ltp": fields.Float(required=True),
    "ltq": fields.Integer(required=True),
})
error_model = ticks_ns.model("Error", {
    "message": fields.String(required=True),
})

@ticks_ns.route("/ticker_prices")
class TickList(Resource):
    @ticks_ns.doc("list_ticks")
    @ticks_ns.param("ticker", "Filter by ticker symbol")
    @ticks_ns.param("start_date", "Start date (YYYY-MM-DD)")
    @ticks_ns.param("end_date", "End date (YYYY-MM-DD)")
    @ticks_ns.param("interval", "Interval (1min or 5min)")
    # @ticks_ns.response(200, "Success", [tick_model]) # Use response instead of marshal
    @ticks_ns.marshal_list_with(tick_model)
    @ticks_ns.response(400, "Bad Request", error_model)
    def get(self):
        """Fetch tick data with filters"""
        ticker = request.args.get("ticker")
        print(ticker)
        if ticker is None:
            return {"message": "Ticker symbol is required"}, 400
        start_date = datetime.fromisoformat(request.args.get("start_date")) if request.args.get("start_date") else None
        end_date = datetime.fromisoformat(request.args.get("end_date")) if request.args.get("end_date") else None
        interval = request.args.get("interval")

        ticks = get_ticks(ticker, start_date, end_date, interval)
        return ticks    


# ticker_list_model = ticks_ns.model("TickerList", fields.List(fields.String))
@ticks_ns.route("/tickers_list")
class TickerList(Resource):
    @ticks_ns.doc("list_tickers")
    # @ticks_ns.marshal_list_with(ticker_list_model)
    def get(self):
        tickers = TickerMaster.query.with_entities(TickerMaster.ticker).all()
        return [ticker[0] for ticker in tickers]