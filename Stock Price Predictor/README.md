# 📈 Stock Price Predictor

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)

</div>

A Python-based machine learning application that predicts next-day stock price trends (up/down) using historical data and technical indicators.

## ✨ Features

- **🔍 Data Collection**: Automatically fetches stock data using Yahoo Finance API
- **📊 Technical Analysis**: Implements various technical indicators:
  - Moving Averages (5, 10, 20 days)
  - Relative Strength Index (RSI)
  - Price volatility measures
  - Volume analysis
  - Price change patterns
- **🤖 Machine Learning**: Uses Random Forest classifier for trend prediction
- **📉 Visualization**: Creates comprehensive charts for analysis
- **💻 Interactive**: Command-line interface for easy usage

## 🚀 Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## 🔧 Usage

### Basic Usage

Run the main script:

```bash
python stock_predictor.py
```

The program will prompt you for:
- Stock symbol (e.g., AAPL, GOOGL, MSFT)
- Time period for historical data (1y, 2y, 5y, max)

### 📝 Example

```bash
$ python stock_predictor.py
Stock Price Predictor
==============================
Enter stock symbol (default: AAPL): GOOGL
Enter time period (1y, 2y, 5y, max) (default: 2y): 2y

Starting Stock Price Prediction Analysis for GOOGL
==================================================
Fetching data for GOOGL...
Successfully fetched 504 days of data
Creating features...
Created 10 features from 490 data points
Training model...
Model trained successfully!
Accuracy: 0.6122

Next Day Prediction for GOOGL:
Direction: UP
Confidence: 65.00%
```

### 💻 Programmatic Usage

You can also use the `StockPredictor` class directly in your code:

```python
from stock_predictor import StockPredictor

# Create predictor instance
predictor = StockPredictor(symbol='AAPL', period='2y')

# Run full analysis
result = predictor.run_full_analysis()

# Or run individual steps
predictor.fetch_data()
predictor.create_features()
predictor.train_model()
prediction = predictor.predict_next_day()
```

## 🌐 Live Preview (Interactive)

Two live options are included:

1. Dash dashboard (rich UI):

```bash
python live_predictor.py
# Then open http://127.0.0.1:8050 in your browser
```

2. Streamlit app (simple, fast live preview):

```bash
streamlit run streamlit_app.py
# Streamlit will print a local URL to open in your browser
```

## 🛠️ Technologies Used

- **Python**: Core programming language
- **yfinance**: Data collection from Yahoo Finance
- **scikit-learn**: Machine learning algorithms
- **pandas & numpy**: Data manipulation and analysis
- **matplotlib, seaborn & plotly**: Data visualization
- **dash**: Interactive web dashboards
- **streamlit**: Interactive app creation

## 👨‍💻 Connect with Me

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)
[![Portfolio](https://img.shields.io/badge/Portfolio-1DA1F2?style=for-the-badge&logo=website&logoColor=white)](https://lively-dodol-cc397c.netlify.app)

</div>

## ❤️ Acknowledgements

Created By ❤️Sunil Sharma❤️

The live preview fetches intraday data (1-minute) for the last 5 days and auto-refreshes every 30 seconds.

## 📊 Technical Indicators Used

1. **Price Change**: Daily percentage change in closing price
2. **High-Low Percentage**: Daily range as percentage of close price
3. **Open-Close Percentage**: Daily movement from open to close
4. **Moving Average Ratios**: Current price relative to 5, 10, and 20-day moving averages
5. **Volatility**: Rolling standard deviation of price changes (5 and 10 days)
6. **Volume Ratio**: Current volume relative to 5-day average volume
7. **RSI**: 14-day Relative Strength Index for momentum analysis

## 🧠 Model Details

- **Algorithm**: Random Forest Classifier
- **Features**: 10 technical indicators
- **Target**: Binary classification (1 for price increase, 0 for decrease)
- **Validation**: 80/20 train-test split with stratification
- **Performance Metrics**: Accuracy, precision, recall, F1-score

## 📋 Output

The program provides:

1. **Model Performance**: Accuracy and detailed classification report
2. **Feature Importance**: Ranking of most influential indicators
3. **Next Day Prediction**: Direction (UP/DOWN) with confidence percentage
4. **Visualizations**: 
   - Price chart with moving averages
   - Trading volume
   - RSI indicator
   - Price change distribution

## ⚠️ Important Notes

**Disclaimer**: This is an educational project for learning machine learning and time series analysis. Stock market predictions are inherently uncertain and this tool should not be used for actual trading decisions without proper risk management and additional analysis.

### Limitations

- Predicts only direction (up/down), not exact price
- Based on historical patterns that may not persist
- Market conditions can change rapidly
- No consideration of external factors (news, earnings, etc.)

## 📚 Learning Objectives

This project helps you learn:

1. **Time Series Analysis**: Working with temporal financial data
2. **Feature Engineering**: Creating meaningful indicators from raw data
3. **Machine Learning**: Classification algorithms and model evaluation
4. **Data Visualization**: Creating informative charts and plots


## 📦 Dependencies

- `yfinance`: Stock data from Yahoo Finance
- `scikit-learn`: Machine learning algorithms
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computing
- `matplotlib`: Plotting and visualization
- `seaborn`: Statistical data visualization
5. **API Integration**: Fetching real-time financial data
6. **Python Programming**: Object-oriented design and best practices

## Future Enhancements

Potential improvements you could implement:

- Add more technical indicators (MACD, Bollinger Bands, etc.)
- Implement different ML algorithms (SVM, Neural Networks)
- Add sentiment analysis from news/social media
- Create a web interface
- Add portfolio analysis capabilities
- Implement backtesting functionality
- Add real-time data updates

## Troubleshooting

### Common Issues

1. **Data Fetching Errors**: Check internet connection and stock symbol validity
2. **Import Errors**: Ensure all dependencies are installed correctly
3. **Memory Issues**: Reduce the time period for large datasets
4. **Plot Display**: Ensure matplotlib backend is properly configured

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed
2. Verify the stock symbol is valid
3. Ensure you have a stable internet connection
4. Check the console output for specific error messages

## License

This project is for educational purposes. Please use responsibly and understand the risks involved in stock market predictions.
