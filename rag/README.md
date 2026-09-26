# 🤖 Crypto Trading Assistant RAG System

## Overview
An intelligent RAG (Retrieval-Augmented Generation) chatbot powered by Google Gemini that answers questions about your cryptocurrency prediction models.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install chromadb langchain langchain-google-genai langchain-community google-generativeai
```

### 2. Run the Notebook
Open `rag.ipynb` and run all cells in order:
1. **Install Libraries** - Install required packages
2. **Configure API** - Gemini API key is already set
3. **Import Components** - Initialize embeddings and LLM
4. **Load Documents** - Index your notebooks
5. **Create Vector Store** - Build ChromaDB database
6. **Setup RAG Chain** - Configure retrieval system
7. **Query Function** - Ready to ask questions!
8. **Test Queries** - Try example questions

### 3. Ask Questions
```python
ask_crypto_assistant("What is Bitcoin's current prediction?")
ask_crypto_assistant("How does the XGBoost model work?")
ask_crypto_assistant("What features are most important?")
```

## 📊 What You Can Ask

### Predictions
- "What's the prediction for Bitcoin today?"
- "Is Ethereum going UP or DOWN?"
- "What's the confidence score for Bitcoin?"

### Model Explanations
- "How does the XGBoost model work?"
- "Explain the SVM binary classification"
- "What is polynomial regression used for?"

### Features & Indicators
- "What features are most important?"
- "Explain RSI and MACD indicators"
- "What are Bollinger Bands?"

### Client Segmentation
- "How are clients segmented?"
- "What's the difference between KMeans and DBSCAN?"
- "What is PCA used for?"

### Model Performance
- "How accurate is the model?"
- "What metrics are used to evaluate predictions?"

## 🔧 Technical Details

### Architecture
- **LLM**: Google Gemini Pro (`gemini-pro`)
- **Embeddings**: Google Generative AI (`models/embedding-001`)
- **Vector DB**: ChromaDB (persistent storage in `./chroma_db`)
- **Framework**: LangChain

### Document Processing
1. Loads all `.ipynb` notebooks from parent directory
2. Extracts markdown and code cells with outputs
3. Splits into 1000-character chunks with 200-char overlap
4. Creates embeddings and stores in ChromaDB
5. Retrieves top 4 relevant chunks per query

### Configuration
- **API Key**: `AIzaSyCNQ-_Va-Q_3RaMzGaLivXK_RrNvZVAKyk` (Google Gemini)
- **Temperature**: 0.3 (balanced creativity)
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Top K Results**: 4 documents

## 📁 Project Structure
```
rag/
├── rag.ipynb              # Main RAG notebook
├── README.md              # This file
└── chroma_db/            # Vector database (created on first run)
```

## 🎯 Features
✅ Natural language question answering  
✅ Context-aware responses with source citations  
✅ Supports multiple notebooks  
✅ Persistent vector storage  
✅ Powered by Google Gemini Pro  

## 🔒 Security Note
The API key is hardcoded for convenience. For production use:
- Store in `.env` file
- Use environment variables
- Never commit API keys to version control

## 📝 Example Output
```
🤔 Question: What is Bitcoin's current prediction?

💡 Answer:
Based on the XGBoost model, Bitcoin is predicted to go UP with a 
confidence score of 0.87. The model uses features like RSI, MACD, 
and Bollinger Bands to make this prediction.

📚 Sources:
  1. ../crypto_price_prediction/crypto_price_prediction.ipynb
  2. ../models/xgboost_model.pkl
```

## 🛠️ Troubleshooting

### ChromaDB Error
If you get a ChromaDB error, delete the `chroma_db` folder and rerun.

### API Key Error
Verify the Gemini API key is correct and has quota remaining.

### No Documents Found
Ensure notebooks exist in parent directory (not just `rag/`).

## 📚 Resources
- [Google Gemini API](https://ai.google.dev/)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
