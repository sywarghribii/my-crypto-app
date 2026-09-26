"""
FastAPI Backend for ML Models
==============================
Provides REST API endpoints for:
1. Crypto Price Predictions (Bitcoin & Ethereum)
2. RAG Chat Assistant (Q&A about models)

Author: ML Analytics Team
Date: 2025-12-13
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from routers import crypto, rag, sentiment

# Initialize FastAPI app
app = FastAPI(
    title="Data Minds API",
    description="REST API for Crypto Predictions, Sentiment Analysis and RAG Chat Assistant",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(crypto.router, prefix="/api/crypto", tags=["Crypto Predictions"])
app.include_router(rag.router, prefix="/api/rag", tags=["RAG Chat Assistant"])
app.include_router(sentiment.router, prefix="/api/sentiment", tags=["Sentiment Analysis"])

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Data Minds API",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": {
            "crypto": "/api/crypto",
            "rag": "/api/rag",
            "docs": "/docs",
            "health": "/health"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "crypto_model": "loaded",
            "rag_assistant": "loaded"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("  Starting Data Minds API Server...")
    print("  URL: http://127.0.0.1:8000")
    print("  Docs: http://127.0.0.1:8000/docs")
    print("="*60 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
