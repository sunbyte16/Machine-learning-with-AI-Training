# 🚀 Complete Setup Guide - Stock Price Predictor

This guide will walk you through setting up the Stock Price Predictor from scratch.

## 📋 Prerequisites

- **Python 3.8 or higher** installed on your system
- **Internet connection** for downloading packages and stock data
- **Command line access** (Terminal/Command Prompt)

### Check Python Installation

```bash
python --version
# or
python3 --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/)

## 🛠️ Installation Methods

### Method 1: Automated Setup (Recommended)

#### For Windows:
```bash
# Double-click setup.bat or run in Command Prompt:
setup.bat
```

#### For Linux/Mac:
```bash
# Make script executable and run:
chmod +x setup.sh
./setup.sh
```

### Method 2: Manual Setup

#### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv stock_predictor_env
stock_predictor_env\Scripts\activate

# Linux/Mac
python3 -m venv stock_predictor_env
source stock_predictor_env/bin/activate
```

#### Step 2: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 3: Test Installation
```bash
python test_installation.py
```

## 🧪 Testing Your Installation

### Quick Test
```bash
python quick_start.py
```

### Full Test
```bash
python test_installation.py
```

### Manual Test
```bash
python stock_predictor.py
```

## 🎯 Running the Application

### Basic Usage
```bash
# Activate virtual environment first
# Windows: stock_predictor_env\Scripts\activate
# Linux/Mac: source stock_predictor_env/bin/activate

python stock_predictor.py
```

### Quick Start Demo
```bash
python quick_start.py
```

## 📁 Project Structure

```
Stock Price Predictor/
├── stock_predictor.py      # Main application
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
├── config.py              # Configuration settings
├── test_installation.py   # Installation test
├── quick_start.py         # Quick demo
├── setup.bat              # Windows setup script
├── setup.sh               # Linux/Mac setup script
├── README.md              # Documentation
└── SETUP_GUIDE.md         # This file
```

## 🔧 Configuration

Edit `config.py` to customize:
- Default stock symbols
- Model parameters
- Time periods
- Plot settings
- Popular stocks list

## 🐛 Troubleshooting

### Common Issues

#### 1. "Python not found"
- **Solution**: Install Python from [python.org](https://www.python.org/downloads/)
- **Windows**: Make sure to check "Add Python to PATH" during installation

#### 2. "pip not found"
```bash
python -m ensurepip --upgrade
```

#### 3. "Permission denied" (Linux/Mac)
```bash
sudo chmod +x setup.sh
```

#### 4. "Module not found" errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 5. "yfinance connection failed"
- Check internet connection
- Try a different stock symbol
- Some symbols might not be available

#### 6. "Matplotlib display issues"
```bash
# For headless servers, install:
pip install matplotlib --upgrade
```

### Getting Help

1. **Check the console output** for specific error messages
2. **Run the test script**: `python test_installation.py`
3. **Try the quick start**: `python quick_start.py`
4. **Check your Python version**: Must be 3.8 or higher

## 🎮 Usage Examples

### Example 1: Basic Prediction
```bash
python stock_predictor.py
# Enter: GOOGL
# Enter: 2y
```

### Example 2: Quick Test
```bash
python quick_start.py
# Choose option 1 for quick test
```

### Example 3: Programmatic Usage
```python
from stock_predictor import StockPredictor

predictor = StockPredictor("TSLA", "1y")
result = predictor.run_full_analysis()
```

## 🔄 Updating the Project

```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Test after update
python test_installation.py
```

## 🗑️ Uninstalling

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment folder
# Windows: rmdir /s stock_predictor_env
# Linux/Mac: rm -rf stock_predictor_env
```

## 📊 What You'll See

After successful setup, you'll get:
- ✅ Stock data fetching
- ✅ Technical indicators calculation
- ✅ Machine learning model training
- ✅ Next-day prediction with confidence
- ✅ Beautiful charts and visualizations
- ✅ Model performance metrics

## 🎓 Learning Path

1. **Start with**: `python quick_start.py`
2. **Try different stocks**: AAPL, GOOGL, TSLA, MSFT
3. **Experiment with time periods**: 1y, 2y, 5y
4. **Read the code**: Understand how it works
5. **Modify parameters**: Edit `config.py`
6. **Add features**: Extend the functionality

## 🚀 Next Steps

- Try different stock symbols
- Experiment with different time periods
- Modify the model parameters in `config.py`
- Add more technical indicators
- Create your own features
- Build a web interface

## 💡 Tips

- **Start small**: Use 1y data for faster testing
- **Popular stocks**: AAPL, GOOGL, MSFT work well
- **Internet required**: For real-time data fetching
- **Be patient**: First run might take a few minutes
- **Save results**: Screenshot the charts for reference

---

**🎉 You're all set! Happy predicting!**

For questions or issues, check the main README.md file or run the test scripts.
