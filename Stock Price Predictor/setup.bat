@echo off
echo ========================================
echo Stock Price Predictor - Windows Setup
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv stock_predictor_env
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    echo Please make sure Python is installed and in your PATH
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call stock_predictor_env\Scripts\activate.bat

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo Step 5: Testing installation...
python test_installation.py
if errorlevel 1 (
    echo Warning: Some tests failed, but installation might still work
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the Stock Price Predictor:
echo 1. Activate the virtual environment: stock_predictor_env\Scripts\activate.bat
echo 2. Run the program: python stock_predictor.py
echo.
echo To deactivate the virtual environment later, just type: deactivate
echo.
pause
