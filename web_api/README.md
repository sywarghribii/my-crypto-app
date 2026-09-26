# ML Analytics Web API

Complete REST API for Machine Learning models with React frontend.

## 🎯 Features

- **Crypto Price Predictions** - Bitcoin & Ethereum daily predictions
- **Client Segmentation** - Customer risk profiling and segmentation
- **Interactive Dashboard** - Modern React UI
- **REST API** - FastAPI backend with automatic documentation

## 📁 Project Structure

```
web_api/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Main application
│   ├── routers/               # API endpoints
│   │   ├── crypto.py         # Crypto predictions endpoints
│   │   └── clients.py        # Client segmentation endpoints
│   ├── services/              # Business logic
│   │   ├── crypto_service.py # Crypto prediction service
│   │   └── client_service.py # Client segmentation service
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React Frontend (to be created)
│   ├── src/
│   │   ├── pages/
│   │   │   ├── CryptoPage.jsx
│   │   │   └── ClientsPage.jsx
│   │   ├── components/
│   │   └── App.jsx
│   └── package.json
│
├── start_backend.bat          # Start FastAPI server
└── README.md                  # This file
```

## 🚀 Quick Start

### Backend Setup

1. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Start Server**
```bash
# Option 1: Using batch file
cd ..
start_backend.bat

# Option 2: Direct command
cd backend
uvicorn main:app --reload --port 8000
```

3. **Access API**
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Frontend Setup (Next Step)

```bash
cd frontend
npm install
npm run dev
```

## 📡 API Endpoints

### Crypto Predictions

- `GET /api/crypto/predictions` - Get current predictions for BTC & ETH
- `GET /api/crypto/predictions/{symbol}` - Get prediction for specific crypto
- `POST /api/crypto/predictions/refresh` - Trigger new predictions
- `GET /api/crypto/history` - Get historical predictions
- `GET /api/crypto/prices/current` - Get current market prices
- `GET /api/crypto/stats` - Get model statistics

### Client Segmentation

- `POST /api/clients/predict` - Predict single client segment
- `POST /api/clients/predict/batch` - Predict multiple clients
- `POST /api/clients/predict/csv` - Upload CSV and predict
- `GET /api/clients/segments` - Get segments information
- `GET /api/clients/stats` - Get model statistics
- `POST /api/clients/recommendations` - Get personalized recommendations

## 📊 Example Requests

### Get Crypto Predictions

```bash
curl http://localhost:8000/api/crypto/predictions
```

Response:
```json
[
  {
    "symbol": "BTC",
    "date": "2025-12-04",
    "current_price": 93527.80,
    "prediction": "HOLD",
    "signal": "HOLD",
    "confidence": 0.625,
    "probabilities": {
      "up": 0.375,
      "down": 0.625
    }
  }
]
```

### Predict Client Segment

```bash
curl -X POST http://localhost:8000/api/clients/predict \
  -H "Content-Type: application/json" \
  -d '{
    "montant_investi": 50000,
    "freq_trading": 25,
    "volatilite_portefeuille": 0.35,
    "periode_detention_moy": 45
  }'
```

Response:
```json
{
  "segment": "Équilibré",
  "risk_score": 5.2,
  "confidence": 0.75,
  "probabilities": {
    "Prudent": 0.15,
    "Équilibré": 0.75,
    "Aventurier": 0.10
  },
  "recommendations": [
    "Équilibre approprié entre risque et rendement",
    "Surveiller régulièrement la volatilité"
  ]
}
```

## 🔧 Configuration

Backend runs on port 8000 by default. To change:

```bash
uvicorn main:app --port 8080
```

CORS is configured for:
- http://localhost:3000 (React default)
- http://localhost:5173 (Vite default)

## 📚 Next Steps

1. ✅ Backend API created
2. ⏭️ Create React frontend
3. ⏭️ Add authentication (optional)
4. ⏭️ Deploy to cloud (Heroku, Railway, etc.)

## 🛠️ Development

### Run in Development Mode

```bash
cd backend
uvicorn main:app --reload
```

### Run Tests

```bash
pytest tests/
```

## 📦 Deployment

### Option 1: Heroku
```bash
heroku create ml-analytics-api
git push heroku main
```

### Option 2: Railway
- Connect GitHub repo
- Railway auto-deploys

### Option 3: Docker
```bash
docker build -t ml-analytics-api .
docker run -p 8000:8000 ml-analytics-api
```

## 📝 License

MIT License - See LICENSE file for details

## 👥 Contact

For questions or support, please contact the ML Analytics Team.
