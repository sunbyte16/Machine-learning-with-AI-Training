"""
Test script to verify Stock Price Predictor installation
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        if package_name:
            importlib.import_module(module_name, package_name)
        else:
            importlib.import_module(module_name)
        print(f"✅ {module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - FAILED: {e}")
        return False

def test_yfinance_connection():
    """Test yfinance connection"""
    try:
        import yfinance as yf
        ticker = yf.Ticker("AAPL")
        data = ticker.history(period="5d")
        if len(data) > 0:
            print("✅ yfinance connection - OK")
            return True
        else:
            print("❌ yfinance connection - FAILED: No data received")
            return False
    except Exception as e:
        print(f"❌ yfinance connection - FAILED: {e}")
        return False

def test_sklearn_functionality():
    """Test scikit-learn functionality"""
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score
        import numpy as np
        
        # Create dummy data
        X = np.random.rand(100, 5)
        y = np.random.randint(0, 2, 100)
        
        # Test train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Test model training
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_train, y_train)
        
        # Test prediction
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print("✅ scikit-learn functionality - OK")
        return True
    except Exception as e:
        print(f"❌ scikit-learn functionality - FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("Stock Price Predictor - Installation Test")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print()
    
    # Test required modules
    modules_to_test = [
        "yfinance",
        "pandas", 
        "numpy",
        "sklearn",
        "matplotlib",
        "seaborn"
    ]
    
    print("Testing module imports:")
    all_imports_ok = True
    for module in modules_to_test:
        if not test_import(module):
            all_imports_ok = False
    
    print()
    print("Testing functionality:")
    
    # Test yfinance connection
    yfinance_ok = test_yfinance_connection()
    
    # Test sklearn functionality
    sklearn_ok = test_sklearn_functionality()
    
    print()
    print("=" * 50)
    
    if all_imports_ok and yfinance_ok and sklearn_ok:
        print("🎉 All tests passed! Installation is successful.")
        print("You can now run: python stock_predictor.py")
        return True
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
        print("Try reinstalling dependencies: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
