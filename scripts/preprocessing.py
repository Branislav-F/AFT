import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def load_data(filename):
    """Load data from a parquet file"""
    data_dir = Path("data")
    file_path = data_dir / f"{filename}.parquet"
    if file_path.exists():
        df = pd.read_parquet(file_path)
        # Ensure 'Date' column is present and set as index if necessary
        if 'Date' in df.columns:
            df.set_index('Date', inplace=True)
        return df
    else:
        print(f"File {filename}.parquet does not exist.")
        return None

def visualize_combined_data(datasets):
    """Visualize combined data in a single graph with the same x-axis and different y-axes"""
    plt.figure(figsize=(12, 6))
    
    for dataset in datasets:
        df = load_data(dataset)
        if df is not None:
            # Check for 'Date' column or use the index if not present
            if 'Date' in df.columns:
                x = df['Date']
            else:
                x = df.index
            
            # Plot the first numeric column found
            y = df.select_dtypes(include='number').iloc[:, 0]
            
            plt.plot(x, y, label=dataset.replace('_', ' ').title())
        else:
            print(f"No data available to visualize for {dataset}.")
    
    plt.title('Combined Data Visualization')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    """Main function to load and visualize data"""
    datasets = ["btc_price", "fear_greed_index", "snp500", "us_dollar_index", "interest_rates"]
    visualize_combined_data(datasets)

if __name__ == "__main__":
    main()

    # nebezi to spravne