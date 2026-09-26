"""
Daily Cryptocurrency Price Prediction Script
============================================
This script fetches live data and generates daily predictions automatically.
Can be scheduled to run daily using Windows Task Scheduler.

Usage:
    python daily_update.py

Output:
    - Console output with predictions
    - predictions_history.csv (appends daily predictions)
"""

import pandas as pd
import numpy as np
import yfinance as yf
import pickle
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def fetch_live_crypto_data(days_back=365):
    """Fetch live cryptocurrency data"""
    print("="*60)
    print("📡 Fetching Live Cryptocurrency Data...")
    print("="*60)
    
    # Calculate date range - use past dates only
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)
    
    cryptos = {
        'BTC-USD': 'BTC',
        'ETH-USD': 'ETH'
    }
    
    all_data = []
    
    for ticker, symbol in cryptos.items():
        print(f"{'🔶' if symbol == 'BTC' else '🔷'} Fetching {ticker}...")
        
        try:
            # Download data using yfinance
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            if len(df) == 0:
                print(f"   ⚠️ Warning: No data received for {symbol}")
                continue
            
            # Handle MultiIndex columns (when downloading single ticker)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Reset index to make Date a column
            df = df.reset_index()
            
            # Remove duplicate columns
            df = df.loc[:, ~df.columns.duplicated()]
            
            # Ensure required columns exist
            expected_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            missing_cols = [col for col in expected_cols if col not in df.columns]
            if missing_cols:
                print(f"   ⚠️ Warning: Missing columns for {symbol}: {missing_cols}")
                continue
            
            # Add 'Adj Close' if missing
            if 'Adj Close' not in df.columns:
                df['Adj Close'] = df['Close']
            
            # Select and reorder columns
            df = df[['Date', 'Adj Close', 'Open', 'High', 'Low', 'Close', 'Volume']]
            
            # Remove rows with NaN in critical columns
            df = df.dropna(subset=['Close', 'High', 'Low', 'Open'])
            
            if len(df) == 0:
                print(f"   ⚠️ Warning: No valid data after cleaning for {symbol}")
                continue
            
            # Add symbol column
            df['symbol'] = symbol
            
            all_data.append(df)
            print(f"   ✓ Successfully fetched {len(df)} records")
            
        except Exception as e:
            print(f"   ❌ Error fetching {symbol}: {str(e)}")
            continue
    
    if not all_data:
        raise ValueError("Failed to fetch data for any cryptocurrency")
    
    # Combine all data
    df_combined = pd.concat(all_data, ignore_index=True)
    df_combined = df_combined.sort_values(['symbol', 'Date']).reset_index(drop=True)
    
    print(f"✓ Data fetched! Latest: {df_combined['Date'].max().date()}")
    return df_combined

def calculate_rsi(data, window=14):
    """Calculate Relative Strength Index"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, fast=12, slow=26, signal=9):
    """Calculate MACD"""
    ema_fast = data.ewm(span=fast, adjust=False).mean()
    ema_slow = data.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    macd_histogram = macd - macd_signal
    return macd, macd_signal, macd_histogram

def engineer_features(df):
    """Create all 44 technical indicators - MATCHES TRAINING EXACTLY"""
    df = df.copy()
    df = df.sort_values(['symbol', 'Date']).reset_index(drop=True)
    
    feature_dfs = []
    
    for symbol in df['symbol'].unique():
        crypto_df = df[df['symbol'] == symbol].copy()
        
        # 1. Price change features
        crypto_df['Daily_Return'] = ((crypto_df['Close'] - crypto_df['Open']) / crypto_df['Open']) * 100
        crypto_df['Price_Change'] = crypto_df['Close'].pct_change() * 100
        crypto_df['Volatility'] = ((crypto_df['High'] - crypto_df['Low']) / crypto_df['Close']) * 100
        
        # 2. Lagged features
        for lag in [1, 2, 3, 5, 7]:
            crypto_df[f'Close_Lag_{lag}'] = crypto_df['Close'].shift(lag)
        
        # 3. Moving Averages
        crypto_df['MA_7'] = crypto_df['Close'].rolling(window=7).mean()
        crypto_df['MA_20'] = crypto_df['Close'].rolling(window=20).mean()
        crypto_df['MA_30'] = crypto_df['Close'].rolling(window=30).mean()
        crypto_df['MA_50'] = crypto_df['Close'].rolling(window=50).mean()
        
        # 4. Moving Average Ratios
        crypto_df['MA_Ratio_7_30'] = crypto_df['MA_7'] / crypto_df['MA_30']
        crypto_df['Price_to_MA7'] = crypto_df['Close'] / crypto_df['MA_7']
        crypto_df['Price_to_MA30'] = crypto_df['Close'] / crypto_df['MA_30']
        
        # 5. Bollinger Bands
        crypto_df['Std_20'] = crypto_df['Close'].rolling(window=20).std()
        crypto_df['Upper_BB'] = crypto_df['MA_20'] + (2 * crypto_df['Std_20'])
        crypto_df['Lower_BB'] = crypto_df['MA_20'] - (2 * crypto_df['Std_20'])
        crypto_df['BB_Position'] = (crypto_df['Close'] - crypto_df['Lower_BB']) / (crypto_df['Upper_BB'] - crypto_df['Lower_BB'])
        
        # 6. Rate of Change
        crypto_df['ROC_5'] = ((crypto_df['Close'] - crypto_df['Close'].shift(5)) / crypto_df['Close'].shift(5)) * 100
        crypto_df['ROC_10'] = ((crypto_df['Close'] - crypto_df['Close'].shift(10)) / crypto_df['Close'].shift(10)) * 100
        
        # 7. RSI
        crypto_df['RSI_14'] = calculate_rsi(crypto_df['Close'], window=14)
        
        # 8. MACD
        crypto_df['MACD'], crypto_df['MACD_Signal'], crypto_df['MACD_Histogram'] = calculate_macd(crypto_df['Close'])
        
        # 9. ATR
        crypto_df['TR1'] = crypto_df['High'] - crypto_df['Low']
        crypto_df['TR2'] = abs(crypto_df['High'] - crypto_df['Close'].shift(1))
        crypto_df['TR3'] = abs(crypto_df['Low'] - crypto_df['Close'].shift(1))
        crypto_df['True_Range'] = crypto_df[['TR1', 'TR2', 'TR3']].max(axis=1)
        crypto_df['ATR_14'] = crypto_df['True_Range'].rolling(window=14).mean()
        crypto_df.drop(['TR1', 'TR2', 'TR3', 'True_Range'], axis=1, inplace=True)
        
        # 10. Volume features
        crypto_df['Volume_Change'] = crypto_df['Volume'].pct_change() * 100
        crypto_df['Volume_MA_7'] = crypto_df['Volume'].rolling(window=7).mean()
        crypto_df['Volume_Ratio'] = crypto_df['Volume'] / crypto_df['Volume_MA_7']
        crypto_df['Volume_ROC_5'] = ((crypto_df['Volume'] - crypto_df['Volume'].shift(5)) / crypto_df['Volume'].shift(5)) * 100
        crypto_df['Volume_Spike'] = (crypto_df['Volume'] > crypto_df['Volume_MA_7'] * 1.5).astype(int)
        
        # 11. Additional indicators
        crypto_df['HL_Spread'] = crypto_df['High'] - crypto_df['Low']
        crypto_df['Rolling_Volatility_7'] = crypto_df['Price_Change'].rolling(window=7).std()
        crypto_df['Rolling_Volatility_30'] = crypto_df['Price_Change'].rolling(window=30).std()
        crypto_df['MA_Cross_Signal'] = (crypto_df['MA_7'] > crypto_df['MA_30']).astype(int)
        crypto_df['Distance_MA7'] = ((crypto_df['Close'] - crypto_df['MA_7']) / crypto_df['MA_7']) * 100
        crypto_df['Distance_MA30'] = ((crypto_df['Close'] - crypto_df['MA_30']) / crypto_df['MA_30']) * 100
        crypto_df['Price_Direction'] = (crypto_df['Close'] > crypto_df['Close'].shift(1)).astype(int)
        crypto_df['Consecutive_Trend'] = crypto_df.groupby((crypto_df['Price_Direction'] != crypto_df['Price_Direction'].shift()).cumsum())['Price_Direction'].transform('count')
        
        feature_dfs.append(crypto_df)
    
    # Combine all cryptocurrencies
    df_with_features = pd.concat(feature_dfs, ignore_index=True)
    
    # Drop NaN rows (from rolling calculations)
    df_with_features = df_with_features.dropna().reset_index(drop=True)
    
    return df_with_features

def load_models():
    """Load trained models"""
    with open('../models/bitcoin_best_model.pkl', 'rb') as f:
        btc_model = pickle.load(f)
    with open('../models/bitcoin_scaler.pkl', 'rb') as f:
        btc_scaler = pickle.load(f)
    with open('../models/ethereum_best_model.pkl', 'rb') as f:
        eth_model = pickle.load(f)
    with open('../models/ethereum_scaler.pkl', 'rb') as f:
        eth_scaler = pickle.load(f)
    with open('../models/feature_columns.pkl', 'rb') as f:
        feature_cols = pickle.load(f)
    
    return btc_model, btc_scaler, eth_model, eth_scaler, feature_cols

def predict(df, btc_model, btc_scaler, eth_model, eth_scaler, feature_cols):
    """Generate predictions"""
    results = []
    
    for symbol in ['BTC', 'ETH']:
        symbol_data = df[df['symbol'] == symbol].copy()
        if len(symbol_data) == 0:
            continue
        
        latest = symbol_data.iloc[-1]
        latest_date = latest['Date']
        current_price = latest['Close']
        
        X_latest = latest[feature_cols].values.reshape(1, -1)
        
        if symbol == 'BTC':
            model, scaler = btc_model, btc_scaler
            threshold_up, threshold_down = 0.70, 0.30
        else:
            model, scaler = eth_model, eth_scaler
            threshold_up, threshold_down = 0.70, 0.30
        
        X_scaled = scaler.transform(X_latest)
        pred_proba = model.predict_proba(X_scaled)[0]
        prob_down, prob_up = pred_proba[0], pred_proba[1]
        
        if prob_up >= threshold_up:
            prediction, signal = "UP", "BUY"
            confidence = prob_up
        elif prob_down >= (1 - threshold_down):
            prediction, signal = "DOWN", "SELL"
            confidence = prob_down
        else:
            prediction, signal = "UNCERTAIN", "HOLD"
            confidence = max(prob_up, prob_down)
        
        results.append({
            'date': latest_date,
            'symbol': symbol,
            'price': current_price,
            'prediction': prediction,
            'signal': signal,
            'confidence': confidence,
            'prob_up': prob_up,
            'prob_down': prob_down
        })
    
    return results

def save_predictions(results):
    """Save predictions to history file"""
    df_results = pd.DataFrame(results)
    
    try:
        # Append to existing file
        df_history = pd.read_csv('../output/predictions_history.csv')
        df_history = pd.concat([df_history, df_results], ignore_index=True)
        df_history = df_history.drop_duplicates(subset=['date', 'symbol'], keep='last')
    except FileNotFoundError:
        # Create new file
        df_history = df_results
    
    df_history.to_csv('../output/predictions_history.csv', index=False)
    print(f"✓ Predictions saved to ../output/predictions_history.csv")

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("🚀 DAILY CRYPTO PRICE PREDICTION")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    # Fetch data
    df = fetch_live_crypto_data(days_back=365)
    
    # Engineer features
    print("\n🔧 Creating technical indicators...")
    df = engineer_features(df)
    print(f"✓ Features ready! Latest date: {df['Date'].max().date()}")
    
    # Load models
    print("\n📦 Loading models...")
    btc_model, btc_scaler, eth_model, eth_scaler, feature_cols = load_models()
    print("✓ Models loaded!")
    
    # Generate predictions
    print("\n🎯 Generating predictions...")
    results = predict(df, btc_model, btc_scaler, eth_model, eth_scaler, feature_cols)
    
    # Display results
    print("\n" + "="*60)
    print("📊 TODAY'S PREDICTIONS")
    print("="*60)
    
    for r in results:
        emoji = "🔶" if r['symbol'] == "BTC" else "🔷"
        name = "Bitcoin" if r['symbol'] == "BTC" else "Ethereum"
        arrow = "⬆️" if r['prediction'] == "UP" else "⬇️" if r['prediction'] == "DOWN" else "⚠️"
        
        print(f"\n{emoji} {name} ({r['symbol']})")
        print(f"   Price: ${r['price']:,.2f}")
        print(f"   Prediction: {r['prediction']} {arrow}")
        print(f"   Signal: {r['signal']}")
        print(f"   Confidence: {r['confidence']*100:.1f}%")
        print(f"   Probabilities: UP={r['prob_up']*100:.1f}% | DOWN={r['prob_down']*100:.1f}%")
    
    # Save to history
    print("\n" + "="*60)
    save_predictions(results)
    
    print("="*60)
    print("✓ Daily update complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
