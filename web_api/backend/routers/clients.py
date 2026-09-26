"""
Client Segmentation API Router
================================
Endpoints for customer risk profiling and segmentation
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import pandas as pd
import io

from services.client_service import ClientService

router = APIRouter()
client_service = ClientService()

# Request/Response Models
class ClientInput(BaseModel):
    montant_investi: float = Field(..., description="Investment amount", gt=0)
    freq_trading: float = Field(..., description="Trading frequency", ge=0)
    volatilite_portefeuille: float = Field(..., description="Portfolio volatility", ge=0)
    periode_detention_moy: float = Field(..., description="Average holding period", ge=0)
    
class ClientPredictionResponse(BaseModel):
    segment: str  # Prudent, Équilibré, Aventurier
    risk_score: float
    confidence: float
    probabilities: Dict[str, float]
    recommendations: List[str]
    features: Dict[str, float]

class BatchClientInput(BaseModel):
    clients: List[ClientInput]

class BatchPredictionResponse(BaseModel):
    total: int
    predictions: List[Dict]

@router.post("/predict", response_model=ClientPredictionResponse)
async def predict_client_segment(client: ClientInput):
    """
    Predict client segment and risk profile
    
    Args:
        client: Client features (investment, frequency, volatility, holding period)
    
    Returns:
        Segment classification with risk score and recommendations
    """
    try:
        prediction = client_service.predict_single_client(client.dict())
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch_clients(batch: BatchClientInput):
    """
    Predict segments for multiple clients
    
    Args:
        batch: List of client data
    
    Returns:
        Predictions for all clients
    """
    try:
        predictions = client_service.predict_batch_clients(
            [client.dict() for client in batch.clients]
        )
        return {
            "total": len(predictions),
            "predictions": predictions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")

@router.post("/predict/csv")
async def predict_from_csv(file: UploadFile = File(...)):
    """
    Upload CSV file and predict segments for all clients
    
    Expected columns:
    - montant_investi
    - freq_trading
    - volatilite_portefeuille
    - periode_detention_moy
    """
    try:
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Validate columns
        required_cols = ['montant_investi', 'freq_trading', 
                        'volatilite_portefeuille', 'periode_detention_moy']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {missing}"
            )
        
        # Predict
        predictions = client_service.predict_from_dataframe(df)
        
        return {
            "total": len(predictions),
            "predictions": predictions,
            "file_name": file.filename
        }
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV processing error: {str(e)}")

@router.get("/segments")
async def get_segments_info():
    """
    Get information about client segments
    """
    return {
        "segments": [
            {
                "name": "Prudent",
                "description": "Conservative investors with low risk tolerance",
                "characteristics": [
                    "Low portfolio volatility",
                    "Long holding periods",
                    "Moderate investment amounts",
                    "Infrequent trading"
                ]
            },
            {
                "name": "Équilibré",
                "description": "Balanced investors with moderate risk tolerance",
                "characteristics": [
                    "Moderate portfolio volatility",
                    "Average holding periods",
                    "Diversified investments",
                    "Regular trading activity"
                ]
            },
            {
                "name": "Aventurier",
                "description": "Aggressive investors with high risk tolerance",
                "characteristics": [
                    "High portfolio volatility",
                    "Short holding periods",
                    "Large investment amounts",
                    "Frequent trading"
                ]
            }
        ]
    }

@router.get("/stats")
async def get_client_statistics():
    """
    Get model statistics and performance metrics
    """
    try:
        stats = client_service.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")

@router.post("/recommendations")
async def get_recommendations(client: ClientInput):
    """
    Get personalized recommendations for a client profile
    """
    try:
        recommendations = client_service.get_recommendations(client.dict())
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendations error: {str(e)}")
