import os
import yfinance as yf

# === Configuration ===
START_DATE = "2018-01-01"
END_DATE = "2025-01-01"
TICKERS = [
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "KOTAKBANK.NS",
    "AXISBANK.NS",
    "PNB.NS",
    "BANKBARODA.NS",
    "INDUSINDBK.NS",
    "IDFCFIRSTB.NS",
    "YESBANK.NS",
    "^NSEBANK"  # Bank Nifty Index
]

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data/raw")

# === To create folder if it doesn’t exist ===
os.makedirs(DATA_DIR, exist_ok=True)

print("=== Banking Sector Data Download ===")
print(f"Period: {START_DATE} to {END_DATE}\n")

# === Download Data ===
for ticker in TICKERS:
    print(f"📥 Downloading data for {ticker} ...")
    data = yf.download(ticker, start=START_DATE, end=END_DATE)

    if not data.empty:
        file_path = os.path.join(DATA_DIR, f"{ticker.replace('^', '')}.csv")
        data.to_csv(file_path)
        print(f"✅ Saved {ticker} data to {file_path}")
    else:
        print(f"⚠️ No data found for {ticker}!")

print("\n✅ All downloads completed! Files saved in /data/raw/")
