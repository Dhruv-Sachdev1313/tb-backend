from app import db

class Tick(db.Model):
    __tablename__ = "ticker_data"
    ts = db.Column(db.DateTime, primary_key=True)
    ticker = db.Column(db.String(10), primary_key=True)
    ltp = db.Column(db.Float, nullable=False)
    ltq = db.Column(db.Integer, nullable=False)
    buy_price = db.Column(db.Float, nullable=False)
    buy_qty = db.Column(db.Integer, nullable=False)
    sell_price = db.Column(db.Float, nullable=False)
    sell_qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Tick {self.ticker} {self.ts}>"
    
class TickerMaster(db.Model):
    __tablename__ = "tickers"
    ticker = db.Column(db.String(10), primary_key=True)
    exchange = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<TickerMaster {self.ticker}>"