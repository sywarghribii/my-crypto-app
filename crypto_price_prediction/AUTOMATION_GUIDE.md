# 🔄 Daily Crypto Price Prediction - Automation Guide

## 📋 Overview
This folder contains scripts to automatically fetch live cryptocurrency data and generate daily predictions using your trained models.

## 📁 Project Structure

```
crypto_price_prediction/
├── models/                      # Trained models and scalers (.pkl files)
├── data/                        # Historical datasets
├── scripts/                     # Automation scripts
│   ├── daily_update.py         # Main Python script
│   ├── run_daily_update.bat    # Windows batch runner
│   └── run_with_anaconda.bat   # Anaconda-specific runner
├── output/                      # Generated predictions
│   └── predictions_history.csv # Prediction tracking
├── crypto_price_prediction.ipynb # Main notebook
├── README.md                    # Project documentation
└── AUTOMATION_GUIDE.md         # This file
```

## 📄 Script Files

1. **`scripts/daily_update.py`** - Main Python script that:
   - Fetches live Bitcoin & Ethereum data from Yahoo Finance
   - Applies the same 44 technical indicators
   - Generates predictions using trained models
   - Saves predictions to `output/predictions_history.csv`

2. **`scripts/run_daily_update.bat`** - Windows batch file to run the script easily

3. **`scripts/run_with_anaconda.bat`** - For Anaconda Python environments

4. **Notebook cells** (at the top) - Interactive version for Jupyter

## 🚀 Quick Start

### Option 1: Run Manually
```bash
# From command line
cd "C:\Users\Aloulou\Desktop\xgboostproject\crypto_price_prediction\scripts"
python daily_update.py
```

Or simply double-click `scripts/run_daily_update.bat`

### Option 2: Run in Notebook
Open `crypto_price_prediction.ipynb` and run the first 5 cells in the "Live Data Updates" section.

## ⏰ Automated Daily Updates with Windows Task Scheduler

### Step-by-Step Setup:

1. **Open Task Scheduler**
   - Press `Win + R`, type `taskschd.msc`, press Enter

2. **Create New Task**
   - Click "Create Basic Task" in the right panel
   - Name: `Crypto Daily Prediction`
   - Description: `Fetch live crypto data and generate daily predictions`

3. **Set Trigger**
   - Choose "Daily"
   - Set time: `09:00 AM` (or after market opens)
   - Recur every: `1 days`

4. **Set Action**
   - Choose "Start a program"
   - Program/script: Browse to `scripts/run_daily_update.bat`
   - Full path: `C:\Users\Aloulou\Desktop\xgboostproject\crypto_price_prediction\scripts\run_daily_update.bat`
   - Start in: `C:\Users\Aloulou\Desktop\xgboostproject\crypto_price_prediction\scripts`

5. **Finish**
   - Check "Open the Properties dialog" to configure more settings

6. **Additional Settings** (in Properties):
   - General tab: ✓ "Run whether user is logged on or not"
   - General tab: ✓ "Run with highest privileges"
   - Settings tab: ✓ "Allow task to be run on demand"
   - Settings tab: ✓ "Run task as soon as possible after a scheduled start is missed"

## 📊 Output

### Console Output
```
============================================================
🚀 DAILY CRYPTO PRICE PREDICTION
📅 2025-12-04 09:00:00
============================================================

📡 Fetching Live Cryptocurrency Data...
✓ Data fetched! Latest: 2025-12-04

🔧 Creating technical indicators...
✓ Features ready!

📦 Loading models...
✓ Models loaded!

🎯 Generating predictions...

============================================================
📊 TODAY'S PREDICTIONS
============================================================

🔶 Bitcoin (BTC)
   Price: $43,521.50
   Prediction: UP ⬆️
   Signal: BUY
   Confidence: 78.5%
   Probabilities: UP=78.5% | DOWN=21.5%

🔷 Ethereum (ETH)
   Price: $2,287.30
   Prediction: DOWN ⬇️
   Signal: SELL
   Confidence: 73.2%
   Probabilities: UP=26.8% | DOWN=73.2%

✓ Predictions saved to predictions_history.csv
============================================================
```

### predictions_history.csv
All daily predictions are saved here with timestamps:

| date | symbol | price | prediction | signal | confidence | prob_up | prob_down |
|------|--------|-------|------------|--------|------------|---------|-----------|
| 2025-12-04 | BTC | 43521.50 | UP | BUY | 0.785 | 0.785 | 0.215 |
| 2025-12-04 | ETH | 2287.30 | DOWN | SELL | 0.732 | 0.268 | 0.732 |

## 🔧 Requirements

Make sure you have these packages installed:
```bash
pip install yfinance pandas numpy xgboost scikit-learn
```

## 📈 Understanding Predictions

### Signals:
- **BUY** ⬆️ - Model predicts price will go UP with high confidence (≥70%)
- **SELL** ⬇️ - Model predicts price will go DOWN with high confidence (≥70%)
- **HOLD** ⚠️ - Model is uncertain, don't trade

### Confidence Thresholds:
- UP prediction needs ≥70% probability
- DOWN prediction needs ≥70% probability
- Otherwise = HOLD (safer strategy)

## 📝 Customization

### Change Update Frequency
Edit the Task Scheduler trigger to run:
- Every hour: Use "Daily" trigger with repeat every 1 hour
- Multiple times per day: Create multiple triggers
- Weekdays only: Add condition in task settings

### Change Confidence Thresholds
Edit in `daily_update.py`:
```python
threshold_up = 0.70    # Change from 70% to your preference
threshold_down = 0.30  # Change from 30% to your preference
```

### Email Notifications
Add email functionality to `daily_update.py`:
```python
import smtplib
# Add email sending code after predictions
```

## 🔍 Monitoring

### Check if Task is Running:
1. Open Task Scheduler
2. Find "Crypto Daily Prediction"
3. Check "Last Run Time" and "Last Run Result"

### View Logs:
- Console output (if running manually)
- Task Scheduler History tab
- predictions_history.csv file

## ⚠️ Troubleshooting

### Task doesn't run:
- Check Task Scheduler is enabled
- Verify Python path is correct
- Ensure all .pkl model files are in the same folder
- Check file permissions

### No internet connection:
- Script will fail to fetch data
- Check network connectivity
- yfinance requires internet access

### Missing model files:
- Run the training notebook first
- Ensure .pkl files are in the same directory
- Files needed: bitcoin_best_model.pkl, ethereum_best_model.pkl, etc.

## 📞 Support

For issues:
1. Check console error messages
2. Verify all model files exist
3. Test `python daily_update.py` manually first
4. Ensure yfinance package is installed

---

**Last Updated**: December 4, 2025
