import os
import pandas as pd
import zipfile
from sqlalchemy import create_engine
import dotenv
from sqlalchemy.exc import IntegrityError

dotenv.load_dotenv()

engine = create_engine(url=os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://user:password@localhost/tick_data"))

def extract_csv_from_zip(zip_path, extract_to="temp_data"):
    """Extract CSV files from a ZIP archive."""
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_to)
    return [os.path.join(extract_to, f) for f in os.listdir(extract_to) if f.endswith(".csv")]

def preprocess_csv(file_path):
    """Read and clean CSV data."""
    df = pd.read_csv(file_path)
    print(df)

    # Remove `.NSE` from ticker
    df["Ticker"] = df["Ticker"].str.replace(".NSE", "", regex=False)

    # Convert Date and Time to single timestamp column
    df["ts"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%Y %H:%M:%S", dayfirst=True)

    df = df.drop(columns=["Date", "Time"])

    return df

def insert_into_db(df):
    """Insert ticker data into TimescaleDB."""
    if df.empty:
        return

    tickers = df[["Ticker"]].drop_duplicates()
    tickers = tickers[["Ticker"]].rename(columns={"Ticker": "ticker"})
    tickers["exchange"] = "NSE"
    try:
        tickers.to_sql("tickers", engine, if_exists="append", index=False, method="multi")
    except IntegrityError:
        pass

    # Insert data into ticker_data
    df.rename(columns={"Ticker": "ticker", "LTP": "ltp", "BuyPrice": "buy_price", 
                       "BuyQty": "buy_qty", "SellPrice": "sell_price", 
                       "SellQty": "sell_qty", "LTQ": "ltq", "OpenInterest": "open_interest"}, inplace=True)
    
    df.to_sql("ticker_data", engine, if_exists="append", index=False, method="multi")

def process_csv(path):
    """Complete ETL pipeline for a ZIP file."""
    csv_files =os.listdir(path)
    for csv_file in csv_files:
        df = preprocess_csv(os.path.join(path, csv_file))
        insert_into_db(df)

if __name__ == "__main__":
    paths = ['data/ticker/STOCK_TICK_04042022', 'data/ticker/STOCK_TICK_05042022']
    for path in paths:
        process_csv(path)
