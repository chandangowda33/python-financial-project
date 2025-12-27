import os 
import pandas as pd

# === paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "../data/raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "../data/processed")
OUTPUT_FILE = os.path.join(PROCESSED_DIR, "combined_banks.csv")

# To create processed folder if missing
os.makedirs(PROCESSED_DIR, exist_ok=True)

# === Helper function to clean CSV file ===
def clean_file(file_path):
    try:
        # Files having multi index so setting header to 3 levels so keeping first row only and changinf price to date
        df = pd.read_csv(file_path, header=0, skiprows=[1, 2])
        df = df.rename(columns={"Price": "Date"})

        # Drop rows without a valid Date
        df = df[df["Date"].str.contains(r"\d", na=False)]

        # Convert Date to datetime
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)

        # Adding new column for ticket(stock name)
        ticker = os.path.basename(file_path).replace(".csv", "")
        df["Ticker"] = ticker

        return df

    except Exception as e:
        print(f"⚠️ Error processing {file_path}: {e}")
        return pd.DataFrame()


def check_file(all_data):
    df=pd.concat(all_data, ignore_index=True)

    # Convert Date to dtypes
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    df["Ticker"] = df["Ticker"].astype("category")
    num_cols = ["Open", "High", "Low", "Close", "Volume"]
    df[num_cols] = df[num_cols].replace({",": ""}, regex=True)
    df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")


    # Keep relevant columns
    df.columns = df.columns.str.lower()
    df = df.dropna(subset=["date"])

    df.sort_values(["date", "ticker"], inplace=True)

    return df

def save_df(df):

    # Saving in csv format for readability and sharing
    df.to_csv(OUTPUT_FILE, index=False)

    # Saving in parquet format for analysis efficiency
    parquet_file = OUTPUT_FILE.replace(".csv", ".parquet")
    df.to_parquet(parquet_file, index=False)

    print(f"\n✅ Combined data saved to: {OUTPUT_FILE}")
    print(f"Total records: {len(df)}")

    return


# Function to load the parquet file and return original df when required
def load_parquet():
    df=pd.read_parquet("../Data/Processed/combined_banks.parquet")
    return df



# === Process all files ===
if __name__ == "__main__":
    all_data = []
    for file in os.listdir(RAW_DIR):
        if file.endswith(".csv"):
            print(f"📂 Cleaning {file} ...")
            file_path = os.path.join(RAW_DIR, file)
            cleaned = clean_file(file_path)
            if not cleaned.empty:
                all_data.append(cleaned)

    # Combine all
    if all_data:
        combined_df=check_file(all_data)
        save_df(combined_df)
        
        
    else:
        print("⚠️ No valid files found in raw folder.")
