import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def load_data(filename):
    """Load data from a parquet file"""
    data_dir = Path("data")
    file_path = data_dir / f"{filename}.parquet"
    if file_path.exists():
        return pd.read_parquet(file_path)
    else:
        print(f"File {filename}.parquet does not exist.")
        return None

def visualize_data(df, title):
    """Visualize data in a graph"""
    if df is not None:
        plt.figure(figsize=(12, 6))
        
        # Check for 'Date' column or use the index if not present
        if 'Date' in df.columns:
            x = df['Date']
        else:
            x = df.index
        
        # Plot the first numeric column found
        y = df.select_dtypes(include='number').iloc[:, 0]
        
        plt.plot(x, y, label=title)
        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print(f"No data available to visualize for {title}.")

def main():
    """Main function to load and visualize data"""
    datasets = ["btc_price", "fear_greed_index", "search_trends", "snp500", "us_dollar_index","interest_rates"]
    
    for dataset in datasets:
        df = load_data(dataset)
        visualize_data(df, dataset.replace('_', ' ').title())

if __name__ == "__main__":
    main()