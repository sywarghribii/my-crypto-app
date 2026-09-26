"""
Sentiment Analysis Router
==========================
REST API endpoints for crypto sentiment analysis.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from services.sentiment_service import SentimentService

router = APIRouter()

# Initialize service
sentiment_service = SentimentService()

# ========================================
# Request/Response Models
# ========================================

class TechnicalPrediction(BaseModel):
    """Technical analysis input"""
    signal: str = Field(..., description="Trading signal (BUY, SELL, HOLD, etc.)")
    pct_change: float = Field(..., description="Expected price change percentage")
    current_price: float = Field(..., description="Current price")
    predicted_price: float = Field(..., description="Predicted price")
    rsi: Optional[float] = Field(50, description="RSI indicator value")

class SentimentRequest(BaseModel):
    """Request for sentiment analysis"""
    crypto: str = Field(..., description="Cryptocurrency name (Bitcoin or Ethereum)")
    technical: TechnicalPrediction = Field(..., description="Technical analysis data")

class SentimentAnalysis(BaseModel):
    """Sentiment analysis results"""
    sentiment: str
    score: float
    confidence: float
    key_factors: List[str]
    reasoning: str

class CombinedSignal(BaseModel):
    """Combined technical + sentiment signal"""
    technical_score: float
    sentiment_score: float
    combined_score: float
    signals_aligned: bool
    tech_weight: float
    sentiment_weight: float

class Recommendation(BaseModel):
    """Final trading recommendation"""
    action: str
    confidence: float
    aligned: bool
    reasoning: str
    timestamp: str

class SentimentResponse(BaseModel):
    """Full sentiment analysis response"""
    crypto: str
    technical: TechnicalPrediction
    sentiment: SentimentAnalysis
    combined_signal: CombinedSignal
    recommendation: Recommendation
    news_count: int
    timestamp: str

# ========================================
# Endpoints
# ========================================

@router.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """
    Analyze crypto sentiment and combine with technical analysis
    
    - Fetches recent news articles
    - Uses Ollama LLM for sentiment analysis
    - Combines with technical signals
    - Generates trading recommendation
    """
    try:
        result = sentiment_service.analyze_crypto(
            crypto_name=request.crypto,
            technical_prediction=request.technical.dict()
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")

@router.post("/clear-cache")
async def clear_cache():
    """Clear the news cache"""
    try:
        sentiment_service.clear_cache()
        return {"status": "success", "message": "News cache cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Ollama connection
        test_response = requests.post(
            sentiment_service.ollama_url,
            json={
                "model": sentiment_service.ollama_model,
                "prompt": "Say OK",
                "stream": False,
                "options": {"num_predict": 5}
            },
            timeout=5
        )
        ollama_status = "ok" if test_response.status_code == 200 else "error"
    except:
        ollama_status = "error"
    
    return {
        "status": "healthy",
        "service": "sentiment_analysis",
        "ollama": ollama_status,
        "model": sentiment_service.ollama_model,
        "timestamp": datetime.now().isoformat()
    }

import requests
