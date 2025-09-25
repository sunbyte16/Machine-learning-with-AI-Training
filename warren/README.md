# 📈 Warren - Stock Price Predictor

<div align="center">

[![Made with Python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Built with Love](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

</div>

## 🎯 About The Project

Stock market prediction is the act of trying to determine the future value of a company stock or other financial instrument traded on an exchange. The successful prediction of a stock's future price could yield significant profit. The efficient-market hypothesis suggests that stock prices reflect all currently available information and any price changes that are not based on newly revealed information thus are inherently unpredictable. Others disagree and those with this viewpoint possess myriad methods and technologies which purportedly allow them to gain future price information.

### 👨‍💻 Created By

Sunil Sharma ❤️

<p align="left">
    <a href="https://github.com/sunbyte16" target="_blank"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
    <a href="https://www.linkedin.com/in/sunil-kumar-bb88bb31a/" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
    <a href="https://lively-dodol-cc397c.netlify.app" target="_blank"><img src="https://img.shields.io/badge/Portfolio-255E63?style=for-the-badge&logo=About.me&logoColor=white" alt="Portfolio"></a>
</p>

## 🚀 Features

We make use of Facebook's Time Series forecasting algorithm Prophet to predict stock market price of US-based companies in real time using multi-variate, single step forecasting strategy.

### 📊 Project Overview
![Header](src/static/images/main_page.png)

## 🛠️ Getting Started

### Prerequisites

- Python 3.7+
- Anaconda (recommended)
- Git

### 📥 Installation

1. Clone the repository
```bash
git clone https://github.com/sunbyte16/warren.git
```

2. Create and activate a project environment (Anaconda recommended)
```bash
conda create --name envname python
conda activate envname
```

3. Install required packages
```bash
pip install -r REQUIREMENTS.txt
```

### 🚀 Running the Application

Navigate to the project directory and run the server:
```bash
cd warren
python runserver.py
```

## 📊 Model Validation Analysis

### 📱 Facebook (Stock: FB) Validation
![FB_validation](src/static/images/fb_forecast_30_day_validation.png)

### 💻 Microsoft (Stock: MSFT) Validation
![MSFT_validation](src/static/images/msft_forecast_30day_validation.png)

### 🔍 Google (Stock: GOOGL) Validation
![GOOGLE_validation](src/static/images/googl_forecast_30day_validation.png)

## ⭐ Support

If you find this project helpful, please consider:
- Giving it a ⭐ star on GitHub
- Forking it to contribute
- Sharing it with others who might find it useful

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
