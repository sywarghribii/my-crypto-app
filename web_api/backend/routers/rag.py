"""
RAG Chat API Router
====================
Endpoints for intelligent Q&A about crypto models using RAG
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

from services.rag_service import RAGService
from services.crypto_service import CryptoService

router = APIRouter()
crypto_service = CryptoService()
rag_service = RAGService(crypto_service=crypto_service)

# Request/Response Models
class ChatRequest(BaseModel):
    question: str = Field(..., description="User's question", min_length=3)
    use_history: bool = Field(True, description="Use chat history for context")

class Source(BaseModel):
    content: str
    metadata: Dict
    relevance: float

class Metrics(BaseModel):
    search_time: float
    generation_time: float
    total_time: float
    num_sources: int

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]
    confidence: float
    metrics: Metrics

class StatsResponse(BaseModel):
    status: str
    documents_count: int
    chat_history_length: int
    model: str
    collection_name: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest):
    """
    Ask a question about crypto prediction models
    
    The RAG system will search the knowledge base and provide
    an informed answer with source citations.
    
    Args:
        request: Question and settings
    
    Returns:
        Answer with sources and performance metrics
    """
    try:
        response = rag_service.ask_question(
            question=request.question
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@router.post("/chat/clear")
async def clear_chat_history():
    """
    Clear the chat history
    
    Removes all previous conversation context
    """
    try:
        result = rag_service.clear_history()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing history: {str(e)}")

@router.get("/stats", response_model=StatsResponse)
async def get_rag_stats():
    """
    Get RAG system statistics
    
    Returns information about the knowledge base and system status
    """
    try:
        stats = rag_service.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

@router.get("/health")
async def health_check():
    """Check RAG service health"""
    try:
        stats = rag_service.get_stats()
        return {
            "status": "healthy",
            "model": stats["model"],
            "documents": stats["total_documents"]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
