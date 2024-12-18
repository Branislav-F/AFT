import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
from pathlib import Path
from pytrends.request import TrendReq 
import time
import requests

import sys
from pathlib import Path

# Add the root directory to the system path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
from config import FRED_API_KEY

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



def fetch_fear_and_greed(start_date=None, end_date=None):
    """Fetch Fear and Greed Index data"""
    base_url = "https://api.alternative.me/fng/"
    
    # Set default dates if not provided
    if end_date is None:
        end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=365)
    
    # Calculate the limit based on the date range
    limit = (end_date - start_date).days
    
    params = {"limit": limit}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame(data["data"])
        df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='s')
        df['value'] = pd.to_numeric(df['value'])
        df = df.sort_values('timestamp')
        
        # Filter the DataFrame based on the provided date range
        df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    
def fetch_snp500(start_date=None, end_date=None):
    """Fetch historical S&P 500 data using yfinance"""
    if end_date is None:
        end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=3650)
    
    snp500 = yf.Ticker("^GSPC")
    df = snp500.history(start=start_date, end=end_date)
    df.reset_index(inplace=True)
    return df

def fetch_us_dollar_index(start_date=None, end_date=None):
    """Fetch historical US Dollar Index (DXY) data using yfinance"""
    if end_date is None:
        end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=365)
    
    dxy = yf.Ticker("DX-Y.NYB")
    df = dxy.history(start=start_date, end=end_date)
    df.reset_index(inplace=True)
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
def save_to_parquet(df, filename):
    """Save DataFrame to parquet file"""
    if df is not None:
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        df.to_parquet(data_dir / f"{filename}.parquet")
    else:
        print(f"Error: Data for {filename} is None and cannot be saved.")

def fetch_interest_rates(start_date=None, end_date=None, api_key=FRED_API_KEY):
    """
    Fetch historical US interest rates from FRED API.

    Args:
        start_date (str): Start date in 'YYYY-MM-DD' format. Default is None.
        end_date (str): End date in 'YYYY-MM-DD' format. Default is None.
        api_key (str): FRED API key.

    Returns:
        DataFrame: DataFrame containing historical interest rates.
    """
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    series_id = "DFF"  # Daily Federal Funds Rate
    
    # Set default dates if not provided
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')
    
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date
    }
    
    try:
        # Print the full URL and parameters for debugging
        print(f"Requesting URL: {base_url}")
        print(f"Parameters: {params}")
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        observations = data.get("observations", [])
        
        # Convert to DataFrame
        df = pd.DataFrame(observations)
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.rename(columns={'date': 'Date', 'value': 'Interest Rate'})
        df = df.sort_values('Date')
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Example usage in main pipeline
def run_data_collection():
    """Main pipeline function"""
    # Calculate date range for the last 10 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3650)
    
    # Fetch data
    btc_data = fetch_btc_price(start_date=start_date, end_date=end_date)
    fg_data = fetch_fear_and_greed(start_date=start_date, end_date=end_date)
    snp500_data = fetch_snp500(start_date=start_date, end_date=end_date)
    us_dollar_index_data = fetch_us_dollar_index(start_date=start_date, end_date=end_date)
    interest_rates_data = fetch_interest_rates(start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))
    
    # Save data
    save_to_parquet(btc_data, "btc_price")
    save_to_parquet(fg_data, "fear_greed_index")
    save_to_parquet(snp500_data, "snp500")
    save_to_parquet(us_dollar_index_data, "us_dollar_index")
    save_to_parquet(interest_rates_data, "interest_rates")
    
    print("Data collection complete.")

if __name__ == "__main__":
    run_data_collection()

