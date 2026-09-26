"""
RAG Chat Service
=================
Provides intelligent Q&A about crypto prediction models using RAG
"""

import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
import time
from typing import Dict, List
import requests
import json

class RAGService:
    def __init__(self, crypto_service=None):
        """Initialize RAG service with ChromaDB and Ollama"""
        self.chat_history = []
        self.crypto_service = crypto_service  # Reference to crypto service for live predictions
        self.db_path = Path(__file__).parent.parent.parent.parent / "rag" / "chroma"
        
        print(f"🔍 Loading ChromaDB from: {self.db_path}")
        
        try:
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(path=str(self.db_path))
            
            # Get or create collection with embedding function
            self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
            
            try:
                self.collection = self.client.get_collection(
                    name="crypto_docs",
                    embedding_function=self.embedding_function
                )
                doc_count = self.collection.count()
                print(f"✓ Loaded existing collection with {doc_count} documents")
            except Exception:
                # Create new collection if doesn't exist
                self.collection = self.client.create_collection(
                    name="crypto_docs",
                    embedding_function=self.embedding_function,
                    metadata={"hnsw:space": "cosine"}
                )
                print("✓ Created new collection")
            
            # Ollama configuration
            self.ollama_url = "http://localhost:11434/api/generate"
            self.model = "llama3.2"
            
            print("✓ RAG service initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing RAG service: {e}")
            raise
    
    def search_documents(self, query: str, n_results: int = 3) -> List[Dict]:
        """Search for relevant documents in ChromaDB"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            documents = []
            if results['documents'] and len(results['documents']) > 0:
                for i, doc in enumerate(results['documents'][0]):
                    distance = results['distances'][0][i] if results.get('distances') else 0
                    
                    # Only include relevant results (distance < 1.5 for cosine similarity)
                    if distance < 1.5:
                        metadata = results['metadatas'][0][i] if results.get('metadatas') else {}
                        documents.append({
                            'content': doc,
                            'metadata': metadata,
                            'distance': distance
                        })
            
            return documents
            
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    def get_live_predictions(self) -> str:
        """Get current crypto predictions from the crypto service"""
        if not self.crypto_service:
            return ""
        
        try:
            predictions = self.crypto_service.get_predictions()
            pred_text = f"\n\nCURRENT LIVE PREDICTIONS:\n"
            pred_text += f"Bitcoin (BTC):\n"
            pred_text += f"  - Current Price: ${predictions['bitcoin']['current_price']:.2f}\n"
            pred_text += f"  - Predicted Price (24h): ${predictions['bitcoin']['predicted_price']:.2f}\n"
            pred_text += f"  - Change: {predictions['bitcoin']['predicted_change']:.2f}%\n"
            pred_text += f"  - Signal: {predictions['bitcoin']['signal']}\n"
            pred_text += f"\nEthereum (ETH):\n"
            pred_text += f"  - Current Price: ${predictions['ethereum']['current_price']:.2f}\n"
            pred_text += f"  - Predicted Price (24h): ${predictions['ethereum']['predicted_price']:.2f}\n"
            pred_text += f"  - Change: {predictions['ethereum']['predicted_change']:.2f}%\n"
            pred_text += f"  - Signal: {predictions['ethereum']['signal']}\n"
            return pred_text
        except Exception as e:
            print(f"Error getting live predictions: {e}")
            return ""
    
    def generate_answer(self, query: str, context: str) -> str:
        """Generate answer using Ollama with live prediction data"""
        try:
            # Get live predictions if available
            live_data = self.get_live_predictions()
            
            prompt = f"""You are a cryptocurrency market analysis system providing educational information about trading signals and model predictions.

CURRENT MODEL PREDICTIONS:
{live_data}

TECHNICAL ANALYSIS REFERENCE:
{context}

ANALYSIS REQUEST: {query}

YOUR TASK: Analyze the current market data and model predictions to provide an educational breakdown of what the signals indicate.

RESPONSE STRUCTURE:

1. MARKET ANALYSIS:
   - Current prices and model predictions
   - Predicted price movement percentages
   - Current signal status (BUY/SELL/HOLD from model)

2. TECHNICAL INTERPRETATION:
   - What the prediction numbers suggest about price direction
   - How to interpret the model's signal
   - Risk/reward calculation based on predicted vs current price

3. EXAMPLE TRADING SCENARIO (Educational):
   Based on these model predictions, here's how a trader might approach this:
   - If BUY signal: "Model suggests upward movement to $X. A trader might consider entry at current price $Y with target $Z"
   - Position sizing example: "With 3% predicted gain, typical allocation would be 5-8% of portfolio"
   - Risk management example: "Stop-loss typically set 3% below entry at $X"

4. IMPORTANT CONTEXT:
   - This is educational analysis of model predictions, not personal advice
   - Always consider your own risk tolerance and financial situation
   - Model accuracy is ~75% historically

REMEMBER: Present this as "what the model predicts" and "how traders typically interpret such signals" rather than direct commands. Use phrases like "the model suggests", "typical approach would be", "historically traders", etc.

Your educational analysis:"""

            # Call Ollama API
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 500
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                return f"Error: Ollama returned status {response.status_code}"
                
        except Exception as e:
            print(f"Error generating answer: {e}")
            return f"Error generating answer: {str(e)}"
    
    def ask_question(self, question: str) -> Dict:
        """
        Main method to ask a question and get an answer with sources
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer, sources, confidence, and performance metrics
        """
        start_time = time.time()
        
        try:
            # Search for relevant documents
            search_start = time.time()
            relevant_docs = self.search_documents(question, n_results=3)
            search_time = time.time() - search_start
            
            if not relevant_docs:
                return {
                    "answer": "I don't have enough information to answer that question. Please ask about crypto predictions, technical indicators, or machine learning models.",
                    "sources": [],
                    "confidence": 0.0,
                    "metrics": {
                        "search_time": search_time,
                        "generation_time": 0,
                        "total_time": time.time() - start_time,
                        "num_sources": 0
                    }
                }
            
            # Prepare context
            context = "\n\n".join([
                f"Source {i+1} (relevance: {1-doc['distance']:.2f}):\n{doc['content']}"
                for i, doc in enumerate(relevant_docs)
            ])
            
            # Generate answer
            gen_start = time.time()
            answer = self.generate_answer(question, context)
            gen_time = time.time() - gen_start
            
            # Calculate confidence based on relevance scores
            avg_distance = sum(doc['distance'] for doc in relevant_docs) / len(relevant_docs)
            confidence = max(0, 1 - avg_distance)  # Convert distance to confidence
            
            # Prepare sources
            sources = [
                {
                    "content": doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content'],
                    "metadata": doc['metadata'],
                    "relevance": round(1 - doc['distance'], 2)
                }
                for doc in relevant_docs
            ]
            
            # Add to chat history
            self.chat_history.append({
                "question": question,
                "answer": answer,
                "timestamp": time.time()
            })
            
            total_time = time.time() - start_time
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": round(confidence, 2),
                "metrics": {
                    "search_time": round(search_time, 3),
                    "generation_time": round(gen_time, 3),
                    "total_time": round(total_time, 3),
                    "num_sources": len(relevant_docs)
                }
            }
            
        except Exception as e:
            print(f"Error in ask_question: {e}")
            return {
                "answer": f"An error occurred: {str(e)}",
                "sources": [],
                "confidence": 0.0,
                "metrics": {
                    "search_time": 0,
                    "generation_time": 0,
                    "total_time": time.time() - start_time,
                    "num_sources": 0
                }
            }
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
        return {"message": "Chat history cleared"}
    
    def get_stats(self) -> Dict:
        """Get statistics about the RAG system"""
        try:
            doc_count = self.collection.count()
            
            return {
                "status": "operational",
                "documents_count": doc_count,
                "chat_history_length": len(self.chat_history),
                "model": self.model,
                "collection_name": self.collection.name
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
