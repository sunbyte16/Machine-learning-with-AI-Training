"""
Stock Price Predictor
A basic machine learning model to predict next-day stock price trends (up/down)
"""

import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class StockPredictor:
    def __init__(self, symbol='AAPL', period='2y'):
        """
        Initialize the Stock Predictor
        
        Args:
            symbol (str): Stock symbol (default: AAPL)
            period (str): Time period for data collection (default: 2y)
        """
        self.symbol = symbol
        self.period = period
        self.data = None
        self.model = None
        self.features = None
        self.target = None
        
    def fetch_data(self):
        """Fetch stock data using yfinance"""
        print(f"Fetching data for {self.symbol}...")
        try:
            ticker = yf.Ticker(self.symbol)
            self.data = ticker.history(period=self.period)
            print(f"Successfully fetched {len(self.data)} days of data")
            return True
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False
    
    def create_features(self):
        """Create technical indicators and features"""
        if self.data is None:
            print("No data available. Please fetch data first.")
            return False
            
        print("Creating features...")
        df = self.data.copy()
        
        # Price-based features
        df['Price_Change'] = df['Close'].pct_change()
        df['High_Low_Pct'] = (df['High'] - df['Low']) / df['Close']
        df['Open_Close_Pct'] = (df['Close'] - df['Open']) / df['Open']
        
        # Moving averages
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_10'] = df['Close'].rolling(window=10).mean()
        df['MA_20'] = df['Close'].rolling(window=20).mean()
        
        # Moving average ratios
        df['MA_5_ratio'] = df['Close'] / df['MA_5']
        df['MA_10_ratio'] = df['Close'] / df['MA_10']
        df['MA_20_ratio'] = df['Close'] / df['MA_20']
        
        # Volatility
        df['Volatility_5'] = df['Price_Change'].rolling(window=5).std()
        df['Volatility_10'] = df['Price_Change'].rolling(window=10).std()
        
        # Volume features
        df['Volume_MA_5'] = df['Volume'].rolling(window=5).mean()
        df['Volume_ratio'] = df['Volume'] / df['Volume_MA_5']
        
        # RSI (Relative Strength Index)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Target variable: Next day price direction (1 for up, 0 for down)
        df['Next_Day_Return'] = df['Close'].shift(-1) / df['Close'] - 1
        df['Target'] = (df['Next_Day_Return'] > 0).astype(int)
        
        # Drop rows with NaN values
        df = df.dropna()
        
        # Select features for training
        feature_columns = [
            'Price_Change', 'High_Low_Pct', 'Open_Close_Pct',
            'MA_5_ratio', 'MA_10_ratio', 'MA_20_ratio',
            'Volatility_5', 'Volatility_10', 'Volume_ratio', 'RSI'
        ]
        
        self.features = df[feature_columns]
        self.target = df['Target']
        self.data = df
        
        print(f"Created {len(feature_columns)} features from {len(df)} data points")
        return True
    
    def train_model(self, test_size=0.2, random_state=42):
        """Train the machine learning model"""
        if self.features is None or self.target is None:
            print("No features available. Please create features first.")
            return False
            
        print("Training model...")
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            self.features, self.target, test_size=test_size, 
            random_state=random_state, stratify=self.target
        )
        
        # Train Random Forest model
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=random_state,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        )
        
        self.model.fit(X_train, y_train)
        
        # Make predictions and evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model trained successfully!")
        print(f"Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.features.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance)
        
        return True
    
    def predict_next_day(self):
        """Predict the next day's price direction"""
        if self.model is None:
            print("No trained model available. Please train the model first.")
            return None
            
        # Get the latest features
        latest_features = self.features.iloc[-1:].values
        
        # Make prediction
        prediction = self.model.predict(latest_features)[0]
        prediction_proba = self.model.predict_proba(latest_features)[0]
        
        direction = "UP" if prediction == 1 else "DOWN"
        confidence = max(prediction_proba) * 100
        
        print(f"\nNext Day Prediction for {self.symbol}:")
        print(f"Direction: {direction}")
        print(f"Confidence: {confidence:.2f}%")
        
        return {
            'direction': direction,
            'confidence': confidence,
            'prediction': prediction,
            'probabilities': prediction_proba
        }
    
    def plot_analysis(self):
        """Create visualization plots"""
        if self.data is None:
            print("No data available for plotting.")
            return
            
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'{self.symbol} Stock Analysis', fontsize=16)
        
        # Price chart with moving averages
        axes[0, 0].plot(self.data.index, self.data['Close'], label='Close Price', linewidth=2)
        axes[0, 0].plot(self.data.index, self.data['MA_5'], label='MA 5', alpha=0.7)
        axes[0, 0].plot(self.data.index, self.data['MA_20'], label='MA 20', alpha=0.7)
        axes[0, 0].set_title('Price and Moving Averages')
        axes[0, 0].set_ylabel('Price ($)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Volume
        axes[0, 1].bar(self.data.index, self.data['Volume'], alpha=0.7, color='orange')
        axes[0, 1].set_title('Trading Volume')
        axes[0, 1].set_ylabel('Volume')
        axes[0, 1].grid(True, alpha=0.3)
        
        # RSI
        axes[1, 0].plot(self.data.index, self.data['RSI'], color='purple', linewidth=2)
        axes[1, 0].axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Overbought')
        axes[1, 0].axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Oversold')
        axes[1, 0].set_title('RSI (Relative Strength Index)')
        axes[1, 0].set_ylabel('RSI')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Price changes distribution
        axes[1, 1].hist(self.data['Price_Change'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        axes[1, 1].set_title('Daily Price Changes Distribution')
        axes[1, 1].set_xlabel('Price Change')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def run_full_analysis(self):
        """Run the complete analysis pipeline"""
        print(f"Starting Stock Price Prediction Analysis for {self.symbol}")
        print("=" * 50)
        
        # Step 1: Fetch data
        if not self.fetch_data():
            return False
            
        # Step 2: Create features
        if not self.create_features():
            return False
            
        # Step 3: Train model
        if not self.train_model():
            return False
            
        # Step 4: Make prediction
        prediction = self.predict_next_day()
        
        # Step 5: Show plots
        self.plot_analysis()
        
        return prediction

def main():
    """Main function to run the stock predictor"""
    print("Stock Price Predictor")
    print("=" * 30)
    
    # Get user input
    symbol = input("Enter stock symbol (default: AAPL): ").strip().upper()
    if not symbol:
        symbol = 'AAPL'
    
    period = input("Enter time period (1y, 2y, 5y, max) (default: 2y): ").strip()
    if not period:
        period = '2y'
    
    # Create predictor and run analysis
    predictor = StockPredictor(symbol=symbol, period=period)
    result = predictor.run_full_analysis()
    
    if result:
        print("\nAnalysis completed successfully!")
    else:
        print("\nAnalysis failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
