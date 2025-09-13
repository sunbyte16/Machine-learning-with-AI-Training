"""
Quick Start Script for Stock Price Predictor
This script provides a simple way to test the predictor with popular stocks
"""

from stock_predictor import StockPredictor
import config

def quick_test():
    """Run a quick test with a popular stock"""
    print("🚀 Stock Price Predictor - Quick Start")
    print("=" * 40)
    
    # Test with Apple stock
    print("Testing with AAPL (Apple Inc.)...")
    predictor = StockPredictor(symbol="AAPL", period="1y")
    
    try:
        result = predictor.run_full_analysis()
        if result:
            print("\n✅ Quick test completed successfully!")
            print("The Stock Price Predictor is working correctly.")
        else:
            print("\n❌ Quick test failed. Please check your internet connection.")
    except Exception as e:
        print(f"\n❌ Error during quick test: {e}")
        print("Please check your installation and try again.")

def interactive_demo():
    """Interactive demo with popular stocks"""
    print("🎯 Interactive Demo - Popular Stocks")
    print("=" * 40)
    
    print("Popular stocks to try:")
    for i, stock in enumerate(config.POPULAR_STOCKS[:10], 1):
        print(f"{i:2d}. {stock}")
    
    print("\nAvailable time periods:")
    for period, description in list(config.TIME_PERIODS.items())[:8]:
        print(f"   {period:4s} - {description}")
    
    print("\nExample usage:")
    print("1. Run: python stock_predictor.py")
    print("2. Enter stock symbol (e.g., GOOGL)")
    print("3. Enter time period (e.g., 2y)")
    print("4. Watch the magic happen! ✨")

def main():
    """Main function"""
    print("Choose an option:")
    print("1. Quick test (AAPL, 1 year)")
    print("2. Show interactive demo info")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        quick_test()
    elif choice == "2":
        interactive_demo()
    elif choice == "3":
        print("Goodbye! 👋")
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
