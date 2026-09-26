"""
Crypto Price Prediction Service
=================================
Business logic for cryptocurrency predictions
"""

import sys
from pathlib import Path
import pandas as pd
import pickle
from datetime import datetime, timedelta
import yfinance as yf
import numpy as np
import threading

# Add project paths
project_root = Path(__file__).parent.parent.parent.parent
crypto_path = project_root / "crypto_price_prediction"
sys.path.append(str(crypto_path))

class CryptoService:
    def __init__(self):
        self.models_path = crypto_path / "models"
        self.output_path = crypto_path / "output"
        self._refresh_lock = threading.Lock()  # Verrou pour éviter écritures simultanées
        self.load_models()
        
    def load_models(self):
        """Load trained models and scalers"""
        try:
            with open(self.models_path / 'bitcoin_best_model.pkl', 'rb') as f:
                self.btc_model = pickle.load(f)
            with open(self.models_path / 'bitcoin_scaler.pkl', 'rb') as f:
                self.btc_scaler = pickle.load(f)
            with open(self.models_path / 'ethereum_best_model.pkl', 'rb') as f:
                self.eth_model = pickle.load(f)
            with open(self.models_path / 'ethereum_scaler.pkl', 'rb') as f:
                self.eth_scaler = pickle.load(f)
            with open(self.models_path / 'feature_columns.pkl', 'rb') as f:
                self.feature_cols = pickle.load(f)
            print("✓ Crypto models loaded successfully")
        except Exception as e:
            print(f"✗ Error loading crypto models: {e}")
            raise
    
    def fetch_live_data(self, days_back=365):
        """Fetch live cryptocurrency data"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        all_data = []
        for ticker, symbol in [('BTC-USD', 'BTC'), ('ETH-USD', 'ETH')]:
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            df = df.reset_index()
            df = df.loc[:, ~df.columns.duplicated()]
            
            if 'Adj Close' not in df.columns:
                df['Adj Close'] = df['Close']
            
            df = df[['Date', 'Adj Close', 'Open', 'High', 'Low', 'Close', 'Volume']]
            df = df.dropna(subset=['Close', 'High', 'Low', 'Open'])
            df['symbol'] = symbol
            all_data.append(df)
        
        return pd.concat(all_data, ignore_index=True)
    
    def engineer_features(self, df):
        """Apply feature engineering (simplified version)"""
        # Import the full feature engineering from the crypto project
        from crypto_price_prediction.scripts.daily_update import (
            calculate_rsi, calculate_macd, engineer_features
        )
        return engineer_features(df)
    
    def get_current_predictions(self):
        """Generate current predictions"""
        try:
            # Fetch and process data
            df = self.fetch_live_data()
            df = self.engineer_features(df)
            
            result = {}
            for symbol in ['BTC', 'ETH']:
                symbol_data = df[df['symbol'] == symbol]
                if len(symbol_data) == 0:
                    continue
                
                latest = symbol_data.iloc[-1]
                X_latest = latest[self.feature_cols].values.reshape(1, -1)
                
                if symbol == 'BTC':
                    model, scaler = self.btc_model, self.btc_scaler
                else:
                    model, scaler = self.eth_model, self.eth_scaler
                
                X_scaled = scaler.transform(X_latest)
                pred_proba = model.predict_proba(X_scaled)[0]
                prob_down, prob_up = pred_proba[0], pred_proba[1]
                
                # Calculate predicted price change
                current_price = float(latest['Close'])
                # Use probability to estimate price change (simplified)
                if prob_up >= 0.70:
                    prediction, signal = "up", "BUY"
                    confidence = prob_up
                    price_change_percent = 2.5  # Estimated increase
                elif prob_down >= 0.70:
                    prediction, signal = "down", "SELL"
                    confidence = prob_down
                    price_change_percent = -2.5  # Estimated decrease
                else:
                    prediction, signal = "neutral", "HOLD"
                    confidence = max(prob_up, prob_down)
                    price_change_percent = 0.5  # Small increase
                
                predicted_price = current_price * (1 + price_change_percent / 100)
                price_change_amount = predicted_price - current_price
                
                # Generate recommendation
                if signal == "BUY":
                    recommendation = f"Strong upward momentum detected. Consider buying {symbol}."
                elif signal == "SELL":
                    recommendation = f"Downward trend anticipated. Consider selling or avoiding {symbol}."
                else:
                    recommendation = f"Market uncertainty. Hold position and monitor {symbol} closely."
                
                result[symbol] = {
                    "current_price": current_price,
                    "next_day_prediction": predicted_price,
                    "predicted_change_percent": price_change_percent,
                    "predicted_change_amount": price_change_amount,
                    "trend": prediction,
                    "signal": signal,
                    "confidence": float(confidence),
                    "recommendation": recommendation,
                    "timestamp": latest['Date'].strftime('%Y-%m-%d')
                }
            
            return result
        except Exception as e:
            print(f"Error generating predictions: {e}")
            raise
    
    def refresh_predictions(self):
        """Refresh predictions and save to history"""
        # Utiliser un verrou pour éviter les écritures simultanées
        with self._refresh_lock:
            predictions = self.get_current_predictions()
            
            # Save to CSV
            history_file = self.output_path / 'predictions_history.csv'
            rows = []
            for symbol, data in predictions.items():
                rows.append({
                    'date': data['timestamp'],
                    'symbol': symbol,
                    'price': data['current_price'],
                    'prediction': data['next_day_prediction'],
                    'signal': data['signal'],
                    'confidence': data['confidence']
                })
            
            df_new = pd.DataFrame(rows)
            
            if history_file.exists():
                try:
                    df_history = pd.read_csv(history_file)
                    # Check if the file is not empty
                    if not df_history.empty:
                        df_history = pd.concat([df_history, df_new], ignore_index=True)
                        df_history = df_history.drop_duplicates(subset=['date', 'symbol'], keep='last')
                    else:
                        df_history = df_new
                except (pd.errors.EmptyDataError, pd.errors.ParserError):
                    # If file is corrupted or empty, start fresh
                    df_history = df_new
            else:
                df_history = df_new
            
            df_history.to_csv(history_file, index=False)
            return predictions
    
    def get_predictions_history(self, symbol=None, limit=30, days=None):
        """Get historical predictions"""
        history_file = self.output_path / 'predictions_history.csv'
        if not history_file.exists():
            return []
        
        try:
            df = pd.read_csv(history_file)
            if df.empty:
                return []
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            return []
        
        if symbol:
            df = df[df['symbol'] == symbol]
        
        if days:
            cutoff_date = datetime.now().date() - timedelta(days=days)
            df['date'] = pd.to_datetime(df['date'])
            df = df[df['date'] >= pd.Timestamp(cutoff_date)]
        
        df = df.sort_values('date', ascending=False).head(limit)
        
        return df.to_dict('records')
    
    def get_current_prices(self):
        """Get current market prices"""
        prices = {}
        for ticker, symbol in [('BTC-USD', 'BTC'), ('ETH-USD', 'ETH')]:
            try:
                data = yf.Ticker(ticker)
                info = data.info
                prices[symbol] = {
                    "current_price": info.get('currentPrice', info.get('regularMarketPrice', 0)),
                    "previous_close": info.get('previousClose', 0),
                    "volume": info.get('volume', 0),
                    "market_cap": info.get('marketCap', 0)
                }
            except:
                prices[symbol] = {"error": "Unable to fetch price"}
        
        return prices
    
    def get_statistics(self):
        """Get model statistics"""
        return {
            "bitcoin_model": {
                "accuracy": 0.854,
                "recall": 0.603,
                "confidence_threshold": "70/30"
            },
            "ethereum_model": {
                "accuracy": 0.766,
                "recall": 0.432,
                "confidence_threshold": "70/30"
            },
            "features": len(self.feature_cols),
            "last_updated": datetime.now().isoformat()
        }
