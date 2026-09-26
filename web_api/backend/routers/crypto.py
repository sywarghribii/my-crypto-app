"""
Crypto Price Prediction API Router
===================================
Endpoints for Bitcoin and Ethereum price predictions
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime, date
import sys
from pathlib import Path

# Import crypto service
from services.crypto_service import CryptoService

router = APIRouter()
crypto_service = CryptoService()

# Request/Response Models
class PredictionResponse(BaseModel):
    symbol: str
    date: str
    current_price: float
    prediction: str  # UP, DOWN, UNCERTAIN
    signal: str  # BUY, SELL, HOLD
    confidence: float
    probabilities: Dict[str, float]
    
class HistoricalPrediction(BaseModel):
    date: str
    symbol: str
    price: float
    prediction: float  # Predicted price value
    signal: str
    confidence: float

class PredictionsHistoryResponse(BaseModel):
    total: int
    predictions: List[HistoricalPrediction]
    
class CryptoPrediction(BaseModel):
    current_price: float
    next_day_prediction: float
    predicted_change_percent: float
    predicted_change_amount: float
    trend: str
    signal: str
    confidence: float
    recommendation: str
    timestamp: str

class PredictionsResponse(BaseModel):
    BTC: CryptoPrediction
    ETH: CryptoPrediction

@router.get("/predictions", response_model=PredictionsResponse)
async def get_current_predictions():
    """
    Get current price predictions for BTC and ETH
    
    Returns latest predictions with confidence scores
    """
    try:
        predictions = crypto_service.get_current_predictions()
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.get("/predictions/{symbol}", response_model=CryptoPrediction)
async def get_prediction_by_symbol(symbol: str):
    """
    Get prediction for specific cryptocurrency
    
    Args:
        symbol: BTC or ETH
    """
    symbol = symbol.upper()
    if symbol not in ['BTC', 'ETH']:
        raise HTTPException(status_code=400, detail="Symbol must be BTC or ETH")
    
    try:
        predictions = crypto_service.get_current_predictions()
        if symbol in predictions:
            return predictions[symbol]
        raise HTTPException(status_code=404, detail=f"No prediction found for {symbol}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/predictions/refresh")
async def refresh_predictions(background_tasks: BackgroundTasks):
    """
    Trigger new prediction generation
    
    Fetches latest data and generates new predictions
    """
    try:
        background_tasks.add_task(crypto_service.refresh_predictions)
        return {
            "status": "refresh_initiated",
            "message": "Predictions are being updated in the background",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refresh error: {str(e)}")

@router.get("/history", response_model=PredictionsHistoryResponse)
async def get_predictions_history(
    symbol: Optional[str] = None,
    limit: int = 30,
    days: Optional[int] = None
):
    """
    Get historical predictions
    
    Args:
        symbol: Filter by BTC or ETH (optional)
        limit: Maximum number of records (default 30)
        days: Filter by last N days (optional)
    """
    try:
        history = crypto_service.get_predictions_history(
            symbol=symbol.upper() if symbol else None,
            limit=limit,
            days=days
        )
        return {
            "total": len(history),
            "predictions": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History error: {str(e)}")

@router.get("/prices/current")
async def get_current_prices():
    """Get current market prices for BTC and ETH"""
    try:
        prices = crypto_service.get_current_prices()
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Price fetch error: {str(e)}")

@router.get("/stats")
async def get_statistics():
    """
    Get prediction statistics and model performance
    """
    try:
        stats = crypto_service.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")
