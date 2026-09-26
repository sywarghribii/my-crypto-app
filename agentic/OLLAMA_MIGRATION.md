# Sentiment Agent: Gemini to Ollama Migration

## ✅ Changes Completed

### 1. **Dependencies Updated**
- **Removed**: `langchain-google-genai` package
- **Kept**: `langgraph`, `langchain-core`, `requests`
- **New Cell 3**: `!pip install langgraph langchain-core requests`

### 2. **Imports Modified**
- **Removed**: 
  - `from langchain_google_genai import ChatGoogleGenerativeAI`
  - `from langchain_core.messages import HumanMessage, SystemMessage`
  - `GEMINI_API_KEY` configuration
- **Added**:
  - `OLLAMA_URL = "http://localhost:11434/api/generate"`
  - `OLLAMA_MODEL = "llama3.2"`

### 3. **Agent Class Refactored**
**CryptoSentimentAgent.__init__():**
- **Before**: Required `gemini_api_key` parameter
- **After**: Takes optional `ollama_url` and `ollama_model` parameters
- **Removed**: ChatGoogleGenerativeAI initialization

**New Method - _call_ollama():**
```python
def _call_ollama(self, prompt: str, timeout: int = 60) -> str:
    """Direct HTTP POST to Ollama API"""
    response = requests.post(
        self.ollama_url,
        json={
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 2000
            }
        },
        timeout=timeout
    )
    return response.json().get("response", "")
```

### 4. **Sentiment Analysis Node Updated**
**_analyze_sentiment_node():**
- **Before**: 
  ```python
  messages = [HumanMessage(content=prompt)]
  response = self.llm.invoke(messages)
  response_text = response.content.strip()
  ```
- **After**:
  ```python
  response_text = self._call_ollama(prompt)
  ```

### 5. **Recommendation Node Updated**
**_generate_recommendation_node():**
- **Before**:
  ```python
  messages = [HumanMessage(content=reasoning_prompt)]
  reasoning_response = self.llm.invoke(messages)
  reasoning = reasoning_response.content.strip()
  ```
- **After**:
  ```python
  reasoning = self._call_ollama(reasoning_prompt)
  ```

### 6. **Agent Initialization Updated**
**Cell 13:**
- **Before**: `agent = CryptoSentimentAgent(gemini_api_key=GEMINI_API_KEY)`
- **After**: `agent = CryptoSentimentAgent()`
- Message: "Using Ollama llama3.2 for sentiment analysis"

### 7. **Documentation Updated**
**Cell 1 (Markdown Header):**
- Title changed to "Crypto Sentiment Analysis Agent - Ollama Version"
- Updated features list:
  - "Uses Ollama llama3.2 model running locally"
  - "Direct HTTP API calls (no LangChain dependency issues)"
- Configuration section:
  - Model: Ollama llama3.2 (Local)
  - API: Direct HTTP to localhost:11434

---

## 🚀 Usage

### Prerequisites
1. **Ollama must be running**: `ollama serve`
2. **Model must be available**: `ollama pull llama3.2`

### Running the Agent
```python
# 1. Import and configure (Cell 5)
# Already set: OLLAMA_URL, OLLAMA_MODEL

# 2. Create agent (Cell 13)
agent = CryptoSentimentAgent()

# 3. Run analysis
technical_prediction = {
    'signal': 'BUY',
    'pct_change': 2.5,
    'current_price': 95000,
    'predicted_price': 97375,
    'rsi': 58.5
}

result = agent.run('Bitcoin', technical_prediction)

# 4. Batch process CSV (Cell 17)
df_enhanced, results = analyze_dataset('combined_crypto_dataset (1).csv', agent)
df_enhanced.to_csv('dataset_with_sentiment.csv', index=False)
```

### Custom Configuration
```python
# Use different Ollama model
agent = CryptoSentimentAgent(
    ollama_url="http://localhost:11434/api/generate",
    ollama_model="llama3.1"  # or any other model
)
```

---

## 🔧 Technical Details

### HTTP Request Format
```json
{
  "model": "llama3.2",
  "prompt": "Your prompt here...",
  "stream": false,
  "options": {
    "temperature": 0.3,
    "num_predict": 2000
  }
}
```

### Response Parsing
- Ollama returns: `{"response": "text here..."}`
- JSON code blocks (```json...```) are automatically stripped
- Response is parsed as JSON for sentiment data

### Error Handling
- Timeout: 60 seconds per request
- Fallback: Returns NEUTRAL sentiment on errors
- No network calls if news fetch fails (uses empty article list)

---

## ⚠️ Notes

1. **No More API Keys**: No external API keys needed for LLM
2. **Local Processing**: All LLM processing happens locally via Ollama
3. **Same Output Format**: Agent returns identical structure as before
4. **Backward Compatible**: All existing analysis functions work unchanged
5. **Performance**: May be slower/faster depending on local hardware vs cloud Gemini

---

## 📊 Benefits of Ollama Migration

✅ **No API Costs**: Free local inference  
✅ **Privacy**: Data never leaves your machine  
✅ **Offline Capable**: Works without internet (except news fetch)  
✅ **No Rate Limits**: No API quotas or throttling  
✅ **Consistent Performance**: Not affected by cloud service issues  
✅ **Customizable**: Can swap models easily  

---

## 🐛 Troubleshooting

### "Connection refused" error
- **Fix**: Start Ollama with `ollama serve`

### "Model not found" error
- **Fix**: Pull model with `ollama pull llama3.2`

### Slow responses
- **Fix**: Reduce `num_predict` in _call_ollama() options
- **Alternative**: Use smaller model like `ollama pull llama3.2:1b`

### JSON parsing errors
- **Check**: Ollama response might need better prompting
- **Solution**: Prompt explicitly states "Return ONLY valid JSON"

---

## 📝 Migration Summary

| Component | Before (Gemini) | After (Ollama) |
|-----------|----------------|----------------|
| **Package** | langchain-google-genai | Direct HTTP |
| **API Key** | Required | Not needed |
| **Model** | gemini-1.5-pro | llama3.2 |
| **Cost** | Pay per token | Free |
| **Network** | Cloud API | Local |
| **Speed** | ~1-2s | Varies (hardware) |
| **Setup** | API key only | Ollama install + model |

---

**Migration completed successfully! ✅**
