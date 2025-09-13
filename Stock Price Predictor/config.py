"""
Configuration file for Stock Price Predictor
"""

# Default settings
DEFAULT_SYMBOL = "AAPL"
DEFAULT_PERIOD = "2y"

# Model parameters
MODEL_PARAMS = {
    'n_estimators': 100,
    'random_state': 42,
    'max_depth': 10,
    'min_samples_split': 5,
    'min_samples_leaf': 2
}

# Feature parameters
FEATURE_PARAMS = {
    'ma_windows': [5, 10, 20],
    'volatility_windows': [5, 10],
    'rsi_period': 14,
    'volume_ma_window': 5
}

# Popular stock symbols for quick testing
POPULAR_STOCKS = [
    "AAPL",  # Apple
    "GOOGL", # Google
    "MSFT",  # Microsoft
    "AMZN",  # Amazon
    "TSLA",  # Tesla
    "META",  # Meta (Facebook)
    "NVDA",  # NVIDIA
    "NFLX",  # Netflix
    "AMD",   # AMD
    "INTC",  # Intel
    "BABA",  # Alibaba
    "V",     # Visa
    "JPM",   # JPMorgan
    "JNJ",   # Johnson & Johnson
    "PG",    # Procter & Gamble
    "KO",    # Coca-Cola
    "PFE",   # Pfizer
    "WMT",   # Walmart
    "DIS",   # Disney
    "ADBE"   # Adobe
]

# Time periods available
TIME_PERIODS = {
    '1d': '1 day',
    '5d': '5 days', 
    '1mo': '1 month',
    '3mo': '3 months',
    '6mo': '6 months',
    '1y': '1 year',
    '2y': '2 years',
    '5y': '5 years',
    '10y': '10 years',
    'ytd': 'Year to date',
    'max': 'Maximum available'
}

# Plot settings
PLOT_SETTINGS = {
    'figsize': (15, 10),
    'dpi': 100,
    'style': 'seaborn-v0_8',
    'colors': {
        'price': '#1f77b4',
        'ma_5': '#ff7f0e', 
        'ma_20': '#2ca02c',
        'volume': '#ff7f0e',
        'rsi': '#9467bd'
    }
}

# RSI thresholds
RSI_THRESHOLDS = {
    'overbought': 70,
    'oversold': 30
}

# Model evaluation settings
EVALUATION_SETTINGS = {
    'test_size': 0.2,
    'random_state': 42,
    'stratify': True
}

# Live preview / streaming settings
LIVE_SETTINGS = {
    'update_interval_seconds': 30,
    'intraday_interval': '1m',
    'intraday_period': '5d'
}
