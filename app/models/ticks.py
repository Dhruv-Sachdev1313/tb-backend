from app import db

class Tick(db.Model):
    __tablename__ = "ticks"
    timestamp = db.Column(db.DateTime, primary_key=True)
    symbol = db.Column(db.String(10), primary_key=True)
    price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    exchange = db.Column(db.String(10))

    def __repr__(self):
        return f"<Tick {self.symbol} {self.timestamp}>"