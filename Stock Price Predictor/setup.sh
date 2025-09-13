#!/bin/bash

echo "========================================"
echo "Stock Price Predictor - Linux/Mac Setup"
echo "========================================"
echo

echo "Step 1: Creating virtual environment..."
python3 -m venv stock_predictor_env
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    echo "Please make sure Python 3 is installed"
    exit 1
fi

echo "Step 2: Activating virtual environment..."
source stock_predictor_env/bin/activate

echo "Step 3: Upgrading pip..."
python -m pip install --upgrade pip

echo "Step 4: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "Step 5: Testing installation..."
python test_installation.py
if [ $? -ne 0 ]; then
    echo "Warning: Some tests failed, but installation might still work"
fi

echo
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo
echo "To run the Stock Price Predictor:"
echo "1. Activate the virtual environment: source stock_predictor_env/bin/activate"
echo "2. Run the program: python stock_predictor.py"
echo
echo "To deactivate the virtual environment later, just type: deactivate"
echo
