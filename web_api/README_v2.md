# Web API - ML Analytics Platform

## 🚀 Updates (v2.0.0)

### New Features:
- ✅ **RAG Chat Assistant** - Intelligent Q&A about crypto prediction models
- ❌ **Removed**: Client Segmentation (replaced with RAG)

### Tech Stack:
- **Backend**: FastAPI + Ollama + ChromaDB
- **Frontend**: React + Vite
- **AI**: RAG (Retrieval-Augmented Generation) with Llama 3.2

---

## 📦 Installation

### Backend Requirements:
```bash
cd backend
pip install fastapi uvicorn chromadb langchain langchain-community
```

### Frontend Requirements:
```bash
cd frontend
npm install
```

### Ollama Setup (Required for RAG):
1. Download from: https://ollama.com/download
2. Install and run: `ollama pull llama3.2`

---

## 🏃 Running the Application

### Option 1: Start All (Windows)
```bash
start_all.bat
```

### Option 2: Manual Start

**Backend:**
```bash
cd backend
python main.py
```
Backend runs at: http://127.0.0.1:8000

**Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs at: http://localhost:5173

---

## 📚 API Endpoints

### Crypto Predictions
- `GET /api/crypto/predictions` - Get BTC & ETH predictions
- `GET /api/crypto/predictions/{symbol}` - Get specific symbol prediction
- `POST /api/crypto/predictions/refresh` - Refresh predictions

### RAG Chat Assistant
- `POST /api/rag/chat` - Ask a question
  ```json
  {
    "question": "What is Bitcoin's prediction?",
    "use_history": true
  }
  ```
- `POST /api/rag/chat/clear` - Clear chat history
- `GET /api/rag/stats` - Get system statistics
- `GET /api/rag/health` - Health check

### General
- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

---

## 🎨 Frontend Features

### Crypto Predictions Tab
- Live Bitcoin & Ethereum price predictions
- Signal recommendations (BUY/SELL/HOLD)
- Confidence scores
- Price change forecasts

### AI Assistant Tab
- **Natural language Q&A** about your models
- **Chat history** for context-aware responses
- **Source citations** for transparency
- **Performance metrics** (search time, confidence)
- **Example questions** to get started

---

## 🔧 Configuration

### Backend (`backend/main.py`)
- CORS origins: Add your frontend URL
- API version and metadata
- Router prefixes

### RAG Service (`backend/services/rag_service.py`)
- ChromaDB path: Points to `rag/chroma_db`
- Model: Ollama Llama 3.2
- Context window: 4096 tokens
- Relevance threshold: 1.5

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'chromadb'"
```bash
pip install chromadb
```

### "RAG Service initialization failed"
1. Make sure you ran the RAG notebook first (`rag/rag.ipynb`)
2. Check that `./rag/chroma_db` folder exists with documents
3. Verify Ollama is running: `ollama list`

### "Cannot connect to Ollama"
1. Make sure Ollama is installed and running
2. Pull the model: `ollama pull llama3.2`
3. Test: `ollama run llama3.2 "hello"`

### Frontend can't connect to backend
1. Check backend is running on port 8000
2. Verify CORS settings in `main.py`
3. Check browser console for errors

---

## 📊 Example Questions for RAG Assistant

- "What is Bitcoin's current prediction?"
- "Explain what RSI and MACD indicators mean"
- "How does the XGBoost model work for crypto prediction?"
- "What features are most important for predictions?"
- "Why did the model predict UP for Ethereum?"
- "How accurate is the model?"

---

## 🔄 Migration from v1.0.0

### Removed:
- Client Segmentation endpoints (`/api/clients/*`)
- `ClientSegmentation.jsx` component
- `client_service.py` and `clients.py` router

### Added:
- RAG Chat endpoints (`/api/rag/*`)
- `RAGChat.jsx` component
- `rag_service.py` and `rag.py` router

### Updated:
- `App.jsx` - Replaced "Client Segmentation" tab with "AI Assistant"
- `main.py` - Updated API description and routers
- `App.css` - Added RAG chat styles

---

## 📝 License

© 2025 ML Analytics | Powered by XGBoost & Ollama RAG
