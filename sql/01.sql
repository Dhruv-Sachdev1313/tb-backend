CREATE TABLE tickers (
    ticker TEXT not NULL,
    exchange TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (ticker)
);
CREATE TABLE ticker_data (
    ticker TEXT NOT NULL REFERENCES tickers(ticker) ON DELETE CASCADE,
    ts TIMESTAMPTZ NOT NULL,
    ltp NUMERIC NOT NULL,
    buy_price NUMERIC NOT NULL,
    buy_qty INTEGER NOT NULL,
    sell_price NUMERIC NOT NULL,
    sell_qty INTEGER NOT NULL,
    ltq INTEGER NOT NULL,
    open_interest INTEGER NOT NULL
);
SELECT create_hypertable('ticker_data', 'ts');
CREATE INDEX ticker_ts_idx ON ticker_data (ticker, ts DESC);
CREATE INDEX ts_idx ON ticker_data (ts DESC);
CREATE INDEX ticker_idx ON ticker_data (ticker DESC);

