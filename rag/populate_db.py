"""
Quick script to populate ChromaDB with crypto documentation
Run this to add sample documents to your RAG system
"""

import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

# Initialize ChromaDB
db_path = Path(__file__).parent / "chroma"
client = chromadb.PersistentClient(path=str(db_path))

# Get or create collection
embedding_function = embedding_functions.DefaultEmbeddingFunction()
try:
    collection = client.get_collection(
        name="crypto_docs",
        embedding_function=embedding_function
    )
    print(f"✓ Found existing collection with {collection.count()} documents")
except:
    collection = client.create_collection(
        name="crypto_docs",
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"}
    )
    print("✓ Created new collection")

# Sample crypto prediction documentation
documents = [
    """Bitcoin (BTC) Price Prediction Model:
    Our XGBoost model uses 10+ technical indicators including RSI, MACD, Bollinger Bands, and trading volume to predict Bitcoin price movements.
    The model achieves 75% accuracy on historical data and updates predictions every 24 hours.
    Key features: 14-day RSI, 12/26-day MACD, 20-day Moving Average, 24h Volume, Market Cap.""",
    
    """Ethereum (ETH) Price Prediction Model:
    Similar to Bitcoin, our Ethereum prediction model leverages machine learning with XGBoost algorithm.
    It analyzes historical price patterns, technical indicators, and market sentiment to forecast ETH price trends.
    The model considers gas prices, network activity, and DeFi metrics unique to Ethereum.""",
    
    """Technical Indicators Explained:
    RSI (Relative Strength Index): Measures momentum on a scale of 0-100. Above 70 indicates overbought, below 30 indicates oversold.
    MACD (Moving Average Convergence Divergence): Shows relationship between two moving averages. Crossovers signal buy/sell opportunities.
    Bollinger Bands: Volatility indicator with upper and lower bands around a moving average.""",
    
    """XGBoost Algorithm:
    XGBoost (Extreme Gradient Boosting) is an ensemble learning method that combines multiple weak prediction models into a strong one.
    It uses gradient boosting framework and is particularly effective for structured/tabular data like financial time series.
    Benefits: High accuracy, handles missing data, prevents overfitting through regularization.""",
    
    """Model Training Process:
    Our models are trained on 2+ years of historical crypto data with daily updates.
    Feature engineering includes technical indicators, volume metrics, and market sentiment scores.
    We use 80/20 train-test split with time-based cross-validation to prevent data leakage.
    Models are retrained monthly to adapt to changing market conditions.""",
    
    """Trading Strategy Recommendations:
    Use predictions as one factor in decision-making, not the sole basis for trades.
    Consider risk management: Never invest more than you can afford to lose.
    Combine technical analysis with fundamental analysis for better insights.
    Set stop-loss orders to limit potential losses. Take profits gradually rather than all at once.""",
    
    """Market Volatility Considerations:
    Crypto markets are highly volatile with rapid price swings.
    Our models perform best in trending markets, less accurate during extreme volatility or black swan events.
    Prediction confidence scores indicate model certainty - lower confidence suggests higher uncertainty.
    Always check multiple timeframes and indicators before making decisions.""",
    
    """Data Sources and Updates:
    Price data sourced from major exchanges via yfinance API.
    Technical indicators calculated using pandas-ta library.
    Models update predictions every 24 hours at midnight UTC.
    Historical accuracy metrics are published monthly on the dashboard.""",
    
    """Trading Signals Interpretation:
    BUY Signal: Model predicts upward price movement. Consider entering long position if:
    - RSI < 70 (not overbought)
    - MACD shows bullish crossover
    - Volume is increasing
    Action: Buy gradually, set stop-loss 2-3% below entry
    
    SELL Signal: Model predicts downward movement. Consider:
    - Taking profits if in profit
    - Avoiding new positions
    - Setting tight stop-losses on existing positions
    Action: Sell in stages, keep 20-30% for potential recovery
    
    HOLD Signal: Unclear direction or low confidence. Best to:
    - Maintain current positions
    - Wait for clearer signals
    - Use this time to review strategy""",
    
    """Decision Support Guidelines:
    When asking about trading decisions, I will:
    1. Analyze current predictions and price trends
    2. Evaluate technical indicators (RSI, MACD, Bollinger Bands)
    3. Consider market volatility and confidence scores
    4. Provide BUY/SELL/HOLD recommendation with clear reasoning
    5. Suggest entry/exit points and stop-loss levels
    6. Remind about risk management (never invest more than you can afford to lose)
    
    Example question: "Should I buy Bitcoin now?"
    I will check current price, predicted price, indicators, and give actionable advice.""",
    
    """Risk Management Rules:
    1. Position Sizing: Never allocate more than 5-10% of portfolio to one asset
    2. Stop Loss: Always set stop-loss at 3-5% below entry for crypto
    3. Take Profit: Scale out profits - sell 25% at 10% gain, 25% at 20%, etc.
    4. Diversification: Split between BTC, ETH, and other assets
    5. Emergency Exit: If loss exceeds 15-20%, exit completely and reassess
    6. FOMO Control: Don't chase pumps, wait for pullbacks to enter
    7. Confidence Check: Only trade when model confidence > 60%"""
]

metadata = [
    {"topic": "bitcoin", "type": "model_description"},
    {"topic": "ethereum", "type": "model_description"},
    {"topic": "technical_indicators", "type": "education"},
    {"topic": "xgboost", "type": "algorithm"},
    {"topic": "training", "type": "methodology"},
    {"topic": "trading", "type": "strategy"},
    {"topic": "risk", "type": "risk_management"},
    {"topic": "data", "type": "infrastructure"},
    {"topic": "signals", "type": "trading_decisions"},
    {"topic": "decision_support", "type": "ai_assistant"},
    {"topic": "risk_rules", "type": "risk_management"}
]

# Add documents
try:
    # Check if already populated
    if collection.count() > 0:
        print(f"⚠️  Collection already has {collection.count()} documents")
        response = input("Do you want to clear and re-populate? (yes/no): ")
        if response.lower() == 'yes':
            client.delete_collection("crypto_docs")
            collection = client.create_collection(
                name="crypto_docs",
                embedding_function=embedding_function,
                metadata={"hnsw:space": "cosine"}
            )
            print("✓ Cleared existing collection")
        else:
            print("❌ Keeping existing documents")
            exit()
    
    # Add documents to collection
    collection.add(
        documents=documents,
        metadatas=metadata,
        ids=[f"doc_{i}" for i in range(len(documents))]
    )
    
    print(f"\n✅ Successfully added {len(documents)} documents to ChromaDB!")
    print(f"📊 Total documents in collection: {collection.count()}")
    print("\n🎉 Your RAG assistant is now ready to answer questions!")
    
except Exception as e:
    print(f"❌ Error: {e}")
