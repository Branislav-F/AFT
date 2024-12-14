# ATF: Financial Market Analysis

ATF is a Python-based project designed to analyze financial market data and predict the price of Bitcoin (BTC) using deep learning models. The project utilizes various indicators such as historical BTC prices, S&P 500 market trends, dollar strength, search engine trends, the Fear and Greed Index, and interest rates to train a Long Short-Term Memory (LSTM) neural network.

## Project Structure
```
project/
│
├── data/                  # Data folder
│   ├── raw/               # Raw data (e.g., downloaded from APIs)
│   └── processed/         # Processed data for model input
│
├── scripts/               # Python scripts for pipeline stages
│   ├── data_collection.py # Fetch financial data
│   ├── preprocessing.py   # Prepare data for model training
│   ├── model.py           # Train and save the LSTM model
│   └── evaluation.py      # Evaluate and visualize model performance
│
├── models/                # Saved machine learning models
│   └── model_lstm.h5      # Trained LSTM model
│
├── results/               # Results and visualizations (e.g., graphs)
│
├── main.py                # Main pipeline for running the project
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Features
- **Data Collection**: Automatically fetch Bitcoin prices, S&P 500 trends, and other financial indicators using APIs.
- **Preprocessing**: Normalize and structure time-series data for deep learning.
- **Model Training**: Train an LSTM model to predict BTC prices based on historical data and additional market indicators.
- **Evaluation**: Compare predictions to actual data and visualize results with interactive graphs.

## Requirements
Ensure you have Python 3.8 or later installed. Install required packages using:
```bash
pip install -r requirements.txt
```

## How to Use
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/atf-project.git
   cd atf-project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the main script:
   ```bash
   python main.py
   ```

## Data Sources
The project collects data from:
- [CoinGecko API](https://www.coingecko.com/en/api)
- [Google Trends](https://trends.google.com/)
- S&P 500 and dollar strength indexes (via relevant financial APIs)

## Results
Model predictions and visualizations are saved in the `results/` directory. Example outputs include:
- Predicted vs. actual BTC prices.
- Graphical evaluation of model performance.

## Future Improvements
- Add more financial indicators (e.g., on-chain metrics).
- Optimize the LSTM model for better performance.
- Deploy the model using a web-based interface.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request for any suggested changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
