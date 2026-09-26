# 📈 Crypto Price Prediction Project

## Overview
Machine learning project that predicts Bitcoin and Ethereum price movements (UP/DOWN) using XGBoost classification models with 44 technical indicators. Includes automated daily prediction system with live data fetching.

## 🎯 Key Results
- **Bitcoin Model:**
  - Accuracy: 85.4%
  - Recall: 60.3%
  - Confidence Threshold: 70/30

- **Ethereum Model:**
  - Accuracy: 76.6%
  - Recall: 43.2%
  - Confidence Threshold: 70/30

## 📁 Project Structure
```
crypto_price_prediction/
├── models/                      # Trained models and scalers
│   ├── bitcoin_best_model.pkl
│   ├── bitcoin_scaler.pkl
│   ├── ethereum_best_model.pkl
│   ├── ethereum_scaler.pkl
│   └── feature_columns.pkl
├── data/                        # Historical datasets
│   └── combined_crypto_dataset.csv
├── scripts/                     # Automation scripts
│   ├── daily_update.py         # Main automation script
│   ├── run_daily_update.bat    # Windows batch runner
│   └── run_with_anaconda.bat   # Anaconda runner
├── output/                      # Generated predictions
│   └── predictions_history.csv
├── crypto_price_prediction.ipynb # Main notebook
├── README.md                    # This file
└── AUTOMATION_GUIDE.md         # Automation setup guide
```

## 🔧 Technical Features
### 44 Technical Indicators Including:
- **Trend Indicators:** SMA, EMA, MACD
- **Momentum:** RSI, Stochastic Oscillator, Williams %R
- **Volatility:** Bollinger Bands, ATR
- **Volume:** OBV, Volume SMA
- **Pattern Recognition:** Price changes, rolling statistics

## 🚀 Usage

### Training Models
1. Open `crypto_price_prediction.ipynb` in Jupyter Notebook or VS Code
2. Run all cells to train models (models are saved to `models/` directory)

### Daily Predictions
**Option 1: Notebook**
- Run the first 5 cells in the "Live Data Updates" section

**Option 2: Command Line**
```bash
cd scripts
python daily_update.py
```

**Option 3: Automated (Windows Task Scheduler)**
- See `AUTOMATION_GUIDE.md` for complete setup instructions
- Double-click `scripts/run_daily_update.bat` to test

## 📊 Model Performance
The models achieve strong accuracy with optimized confidence thresholds. Bitcoin model shows excellent balance between precision and recall, while Ethereum model is more conservative (lower recall reflects model uncertainty on UP movements).

## 💡 Applications
- Trading signal generation
- Risk management
- Portfolio optimization
- Market trend analysis
- Automated daily predictions with live data
