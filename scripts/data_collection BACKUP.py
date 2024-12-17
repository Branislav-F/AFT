import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
from pathlib import Path

def fetch_btc_price(start_date=None, end_date=None):
    """
    Fetch Bitcoin historical prices
    Returns DataFrame with columns: Date, Open, High, Low, Close, Volume
    """
    if end_date is None:
        end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=10*365)
    
    btc = yf.Ticker("BTC-USD")
    df = btc.history(start=start_date, end=end_date)
    df.reset_index(inplace=True)
    return df

def fetch_fear_and_greed(limit=0):
    """
    Fetch Fear and Greed Index data from alternative.me API
    Args:
        limit (int): Number of days (0 = all available data)
    Returns:
        DataFrame with columns: timestamp, value, classification
    """
    base_url = "https://api.alternative.me/fng/"
    params = {"limit": limit}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data["metadata"]["error"]:
            raise ValueError(f"API Error: {data['metadata']['error']}")
            
        # Convert to DataFrame
        df = pd.DataFrame(data["data"])
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='s')
        
        # Convert value to numeric
        df['value'] = pd.to_numeric(df['value'])
        
        # Sort by timestamp
        df = df.sort_values('timestamp')
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


# Function: fetch_snp500
# Description: Fetch historical S&P 500 data using a financial API (e.g., Alpha Vantage). 
# Returns a DataFrame containing `timestamp` and `price`.
def fetch_snp500(api_key):
    # TODO: Implement API call to fetch S&P 500 data
    pass

def save_to_parquet(df, filename):
    """Save DataFrame to parquet file"""
    df.to_parquet(f"data/{filename}.parquet")

def visualize_data(df, title="Bitcoin Price History"):
    """Create price visualization"""
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Close'], label='BTC Price', color='orange')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt

def visualize_fear_and_greed(df):
    """
    Create visualization of Fear and Greed Index
    Args:
        df: DataFrame with columns: timestamp, value, classification
    """
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Color mapping based on value ranges
    colors = ['#FF0000' if x <= 25 else '#FFA500' if x <= 50 
             else '#90EE90' if x <= 75 else '#008000' for x in df['value']]
    
    # Create bar plot
    plt.bar(df['timestamp'], df['value'], color=colors)
    
    # Add horizontal lines for fear/greed zones
    plt.axhline(y=25, color='r', linestyle='--', alpha=0.3)
    plt.axhline(y=50, color='gray', linestyle='--', alpha=0.3)
    plt.axhline(y=75, color='g', linestyle='--', alpha=0.3)
    
    # Customize plot
    plt.title('Bitcoin Fear and Greed Index')
    plt.xlabel('Date')
    plt.ylabel('Index Value')
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#FF0000', label='Extreme Fear (0-25)'),
        Patch(facecolor='#FFA500', label='Fear (26-50)'),
        Patch(facecolor='#90EE90', label='Greed (51-75)'),
        Patch(facecolor='#008000', label='Extreme Greed (76-100)')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    return plt

def run_data_collection():
    """Main pipeline function"""
    # Fetch data
    btc_data = fetch_btc_price()
    fg_data = fetch_fear_and_greed()
    
    # Create visualizations
    btc_plot = visualize_data(btc_data)
    btc_plot.savefig('data/btc_price.png')
    
    if fg_data is not None:
        fg_plot = visualize_fear_and_greed(fg_data)
        fg_plot.savefig('data/fear_greed.png')
    
    plt.show()

def save_fear_greed_data(df, filename="fear_greed_index"):
    """Save Fear and Greed data to parquet"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    df.to_parquet(data_dir / f"{filename}.parquet")

def load_btc_data(filename="btc_price"):
    """Load Bitcoin price data from parquet"""
    data_dir = Path("data")
    file_path = data_dir / f"{filename}.parquet"
    
    try:
        if file_path.exists():
            return pd.read_parquet(file_path)
        else:
            # If file doesn't exist, fetch and save new data
            btc_data = fetch_btc_price()
            data_dir.mkdir(exist_ok=True)
            btc_data.to_parquet(file_path)
            return btc_data
    except Exception as e:
        print(f"Error loading BTC data: {e}")
        return None

def load_fear_greed_data(filename="fear_greed_index"):
    """Load Fear and Greed data from parquet"""
    data_dir = Path("data")
    file_path = data_dir / f"{filename}.parquet"
    if file_path.exists():
        return pd.read_parquet(file_path)
    return None

def create_combined_visualization(btc_df, fg_df):
    """Create combined BTC price and Fear&Greed visualization"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), height_ratios=[2, 1])
    
    # Plot BTC price on top subplot
    ax1.plot(btc_df['Date'], btc_df['Close'], color='orange', label='BTC Price')
    ax1.set_title('Bitcoin Price History')
    ax1.set_xlabel('')
    ax1.set_ylabel('Price (USD)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot Fear & Greed on bottom subplot
    colors = ['#FF0000' if x <= 25 else '#FFA500' if x <= 50 
             else '#90EE90' if x <= 75 else '#008000' for x in fg_df['value']]
    
    ax2.bar(fg_df['timestamp'], fg_df['value'], color=colors)
    ax2.axhline(y=25, color='r', linestyle='--', alpha=0.3)
    ax2.axhline(y=50, color='gray', linestyle='--', alpha=0.3)
    ax2.axhline(y=75, color='g', linestyle='--', alpha=0.3)
    
    ax2.set_title('Fear and Greed Index')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Index Value')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    
    # Add Fear & Greed legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#FF0000', label='Extreme Fear'),
        Patch(facecolor='#FFA500', label='Fear'),
        Patch(facecolor='#90EE90', label='Greed'),
        Patch(facecolor='#008000', label='Extreme Greed')
    ]
    ax2.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    return plt

def run_data_pipeline():
    """Main execution pipeline"""
    # Load or fetch data
    btc_data = load_btc_data()
    if btc_data is None:
        print("Failed to load BTC data")
        return
        
    fg_data = fetch_fear_and_greed()
    if fg_data is None:
        print("Failed to load Fear & Greed data")
        return
    
    # Verify data exists before visualization
    if len(btc_data) > 0 and len(fg_data) > 0:
        plot = create_combined_visualization(btc_data, fg_data)
        plot.savefig('data/combined_analysis.png')
        plot.show()
    else:
        print("No data available for visualization")

if __name__ == "__main__":
    run_data_pipeline()

    