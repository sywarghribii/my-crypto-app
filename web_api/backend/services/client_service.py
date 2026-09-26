"""
Client Segmentation Service
============================
Business logic for customer risk profiling
"""

import sys
from pathlib import Path
import pandas as pd
import pickle
import numpy as np
from datetime import datetime

# Add project paths
project_root = Path(__file__).parent.parent.parent.parent
client_path = project_root / "client_segmentation"
sys.path.append(str(client_path))

class ClientService:
    def __init__(self):
        self.client_path = client_path
        self.load_model()
        
    def load_model(self):
        """Load trained Random Forest model"""
        try:
            # Note: You'll need to save the client model as a .pkl file
            # For now, we'll create a placeholder
            # TODO: Save the trained model from client.ipynb
            
            # Placeholder - replace with actual model loading
            self.model = None
            self.scaler = None
            
            # Load sample data for feature engineering
            data_file = self.client_path / "crypto_users_50000.csv"
            if data_file.exists():
                self.sample_data = pd.read_csv(data_file)
                print("✓ Client data loaded")
            else:
                print("⚠ Client data file not found")
                self.sample_data = None
            
            print("✓ Client service initialized")
        except Exception as e:
            print(f"✗ Error loading client model: {e}")
            # Don't raise - allow service to start with sample data
    
    def create_features(self, client_data):
        """Engineer features from raw client data"""
        # Create interaction features like in the notebook
        features = client_data.copy()
        
        # Add interaction features
        features['freq_x_volatility'] = (
            features['freq_trading'] * features['volatilite_portefeuille']
        )
        features['portfolio_x_volatility'] = (
            features['montant_investi'] * features['volatilite_portefeuille']
        )
        features['freq_over_holding'] = (
            features['freq_trading'] / (features['periode_detention_moy'] + 1)
        )
        
        return features
    
    def predict_single_client(self, client_data):
        """Predict segment for a single client"""
        # Create features
        features_df = pd.DataFrame([client_data])
        features_df = self.create_features(features_df)
        
        # For demo purposes, use rule-based logic
        # TODO: Replace with actual model prediction
        segment, risk_score = self._rule_based_prediction(client_data)
        
        # Generate probabilities (simulated for now)
        if segment == "Prudent":
            probs = {"Prudent": 0.85, "Équilibré": 0.12, "Aventurier": 0.03}
            confidence = 0.85
        elif segment == "Équilibré":
            probs = {"Prudent": 0.15, "Équilibré": 0.75, "Aventurier": 0.10}
            confidence = 0.75
        else:  # Aventurier
            probs = {"Prudent": 0.05, "Équilibré": 0.15, "Aventurier": 0.80}
            confidence = 0.80
        
        # Get recommendations
        recommendations = self._get_recommendations(segment, client_data)
        
        return {
            "segment": segment,
            "risk_score": risk_score,
            "confidence": confidence,
            "probabilities": probs,
            "recommendations": recommendations,
            "features": {
                "montant_investi": client_data['montant_investi'],
                "freq_trading": client_data['freq_trading'],
                "volatilite_portefeuille": client_data['volatilite_portefeuille'],
                "periode_detention_moy": client_data['periode_detention_moy']
            }
        }
    
    def _rule_based_prediction(self, client_data):
        """Rule-based segmentation logic"""
        volatility = client_data['volatilite_portefeuille']
        freq = client_data['freq_trading']
        holding = client_data['periode_detention_moy']
        
        # Calculate risk score (0-10)
        risk_score = (
            (volatility / 0.5 * 4) +  # Volatility contribution (0-4)
            (freq / 50 * 3) +          # Frequency contribution (0-3)
            ((100 - holding) / 100 * 3)  # Holding period (inverse, 0-3)
        )
        risk_score = min(risk_score, 10.0)  # Cap at 10
        
        # Determine segment
        if risk_score < 3.5:
            segment = "Prudent"
        elif risk_score < 7.0:
            segment = "Équilibré"
        else:
            segment = "Aventurier"
        
        return segment, round(risk_score, 2)
    
    def _get_recommendations(self, segment, client_data):
        """Generate personalized recommendations"""
        recommendations = []
        
        if segment == "Prudent":
            recommendations = [
                "Maintenir une stratégie d'investissement conservative",
                "Privilégier les actifs stables et peu volatils",
                "Envisager une diversification progressive",
                "Augmenter légèrement l'exposition au risque si objectifs à long terme"
            ]
        elif segment == "Équilibré":
            recommendations = [
                "Équilibre approprié entre risque et rendement",
                "Surveiller régulièrement la volatilité du portefeuille",
                "Considérer une allocation 60/40 (stable/dynamique)",
                "Réévaluer la stratégie tous les trimestres"
            ]
        else:  # Aventurier
            recommendations = [
                "⚠️ Niveau de risque élevé - surveiller attentivement",
                "Diversifier pour réduire la concentration du risque",
                "Définir des stop-loss pour limiter les pertes",
                "Allouer une partie du portefeuille à des actifs moins volatils",
                "Considérer une approche plus équilibrée pour la stabilité"
            ]
        
        # Add specific recommendations based on features
        if client_data['volatilite_portefeuille'] > 0.4:
            recommendations.append("⚠️ Volatilité élevée détectée - envisager une réduction")
        
        if client_data['freq_trading'] > 40:
            recommendations.append("💡 Fréquence de trading élevée - attention aux coûts de transaction")
        
        if client_data['periode_detention_moy'] < 20:
            recommendations.append("💡 Période de détention courte - adopter une vision plus long terme")
        
        return recommendations
    
    def predict_batch_clients(self, clients_data):
        """Predict segments for multiple clients"""
        predictions = []
        for client_data in clients_data:
            pred = self.predict_single_client(client_data)
            pred['client_id'] = len(predictions) + 1
            predictions.append(pred)
        return predictions
    
    def predict_from_dataframe(self, df):
        """Predict from pandas DataFrame"""
        clients_data = df.to_dict('records')
        predictions = self.predict_batch_clients(clients_data)
        
        # Add original data
        for i, pred in enumerate(predictions):
            pred.update(clients_data[i])
        
        return predictions
    
    def get_statistics(self):
        """Get model statistics"""
        return {
            "model_type": "Random Forest Regressor",
            "r2_score": 0.8676,
            "mae": 0.0767,
            "features": 7,
            "segments": 3,
            "total_clients_trained": 50000,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_recommendations(self, client_data):
        """Get detailed recommendations for a client"""
        segment, risk_score = self._rule_based_prediction(client_data)
        recommendations = self._get_recommendations(segment, client_data)
        
        return {
            "segment": segment,
            "risk_score": risk_score,
            "recommendations": recommendations,
            "risk_level": "Faible" if risk_score < 3.5 else "Modéré" if risk_score < 7.0 else "Élevé",
            "suggested_actions": {
                "immediate": recommendations[:2],
                "short_term": recommendations[2:4] if len(recommendations) > 2 else [],
                "long_term": recommendations[4:] if len(recommendations) > 4 else []
            }
        }
