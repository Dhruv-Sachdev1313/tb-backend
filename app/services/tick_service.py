from app.models import Tick
from datetime import datetime

def get_ticks(ticker, start_date=None, end_date=None, interval=None):
    query = Tick.query.filter(Tick.ticker==ticker)
    if start_date:
        query = query.filter(Tick.ts >= start_date)
    if end_date:
        query = query.filter(Tick.ts <= end_date)

    # Execute query
    ticks = query.all()

    # Apply interval grouping (basic example for 1-min or 5-min)
    if interval:
        grouped_ticks = {}
        for tick in ticks:
            if interval == "1min":
                key = tick.ts.replace(second=0, microsecond=0)
            elif interval == "5min":
                key = tick.ts.replace(minute=(tick.ts.minute // 5) * 5, second=0, microsecond=0)
            if key not in grouped_ticks:
                grouped_ticks[key] = []
            grouped_ticks[key].append(tick)
        return grouped_ticks

    return ticks