import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
from pathlib import Path

def fetch_btc_price(start_date=None, end_date=None):
    """Fetch Bitcoin historical prices"""
    if end_date is None:
        end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=365)
    
    btc = yf.Ticker("BTC-USD")
    df = btc.history(start=start_date, end=end_date)
    df.reset_index(inplace=True)
    return df

def fetch_search_trends():
    """Fetch Bitcoin search engine trends"""
    # Placeholder implementation
    data = {
        'Date': [datetime.now() - timedelta(days=i) for i in range(10)],
        'Trends': [i for i in range(10)]
    }
    df = pd.DataFrame(data)
    return df

def fetch_fear_and_greed(limit=0):
    """Fetch Fear and Greed Index data"""
    base_url = "https://api.alternative.me/fng/"
    params = {"limit": limit}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame(data["data"])
        df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='s')
        df['value'] = pd.to_numeric(df['value'])
        df = df.sort_values('timestamp')
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def fetch_snp500(start_date=None, end_date=None):
    """Fetch historical S&P 500 data using yfinance"""
    if end_date is None:
        end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=365)
    
    snp500 = yf.Ticker("^GSPC")
    df = snp500.history(start=start_date, end=end_date)
    df.reset_index(inplace=True)
    return df

def fetch_dollar_strength():
    """Fetch Dollar strength data"""
    # Placeholder implementation
    data = {
        'Date': [datetime.now() - timedelta(days=i) for i in range(10)],
        'Strength': [i for i in range(10)]
    }
    df = pd.DataFrame(data)
    return df

def save_to_parquet(df, filename):
    """Save DataFrame to parquet file"""
    if df is not None:
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        df.to_parquet(data_dir / f"{filename}.parquet")
    else:
        print(f"Error: Data for {filename} is None and cannot be saved.")

# Example usage in main pipeline
def run_data_collection():
    """Main pipeline function"""
    # Fetch data
    btc_data = fetch_btc_price()
    search_trends_data = fetch_search_trends()
    fg_data = fetch_fear_and_greed()
    snp500_data = fetch_snp500()
    dollar_strength_data = fetch_dollar_strength()
    
    # Save data
    save_to_parquet(btc_data, "btc_price")
    save_to_parquet(search_trends_data, "search_trends")
    save_to_parquet(fg_data, "fear_greed_index")
    save_to_parquet(snp500_data, "snp500")
    save_to_parquet(dollar_strength_data, "dollar_strength")
    
    print("Data collection complete.")

if __name__ == "__main__":
    run_data_collection()