# Configuration for Crypto Sentiment Agent - Optimized Version

# =============================================================================
# API CONFIGURATION
# =============================================================================

# Google Gemini API
GEMINI_MODEL = "gemini-1.5-flash"  # Free tier model
GEMINI_TEMPERATURE = 0.3           # Lower = more consistent
GEMINI_MAX_OUTPUT_TOKENS = 2000    # Sufficient for sentiment analysis
GEMINI_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your key

# News API
NEWS_SOURCE = "cryptopanic"        # Options: cryptopanic, mock
NEWS_API_URL = "https://cryptopanic.com/api/v1/posts/"
NEWS_AUTH_TOKEN = "free"           # Use free public feed
NEWS_TIMEOUT = 10                  # Request timeout in seconds
NEWS_MAX_ARTICLES = 10             # Number of articles to fetch

# =============================================================================
# CACHING CONFIGURATION
# =============================================================================

ENABLE_NEWS_CACHE = True           # Cache news articles per crypto
ENABLE_SENTIMENT_CACHE = True      # Cache sentiment analysis results
CACHE_TTL = 900                    # Time-to-live in seconds (15 minutes)
AUTO_CLEAR_CACHE = False           # Clear cache on agent restart

# =============================================================================
# BATCH PROCESSING CONFIGURATION
# =============================================================================

DEFAULT_SAMPLE_SIZE = None         # None = all rows, int = number of rows
CRYPTO_COLUMN_NAMES = [            # Possible crypto column names
    'Crypto', 'crypto',
    'Currency', 'currency',
    'Symbol', 'symbol',
    'Coin', 'coin'
]

# Output columns to add
OUTPUT_COLUMNS = [
    'Sentiment',              # BULLISH, BEARISH, NEUTRAL
    'Sentiment_Score',        # -100 to +100
    'Sentiment_Confidence',   # 0 to 1
    'Key_Factors'            # Comma-separated factors
]

# =============================================================================
# SIGNAL COMBINATION WEIGHTS
# =============================================================================

TECHNICAL_WEIGHT = 0.6             # 60% weight on technical signals
SENTIMENT_WEIGHT = 0.4             # 40% weight on sentiment signals

# Signal alignment thresholds
STRONG_BUY_THRESHOLD = 60          # Combined score > 60
BUY_THRESHOLD = 30                 # Combined score > 30
STRONG_SELL_THRESHOLD = -60        # Combined score < -60
SELL_THRESHOLD = -30               # Combined score < -30

# Confidence adjustments
ALIGNED_CONFIDENCE_BOOST = 0.95    # When signals agree
ALIGNED_CONFIDENCE_BASE = 0.75     # Base confidence when aligned
CONFLICTING_CONFIDENCE = 0.5       # When signals conflict
NEUTRAL_CONFIDENCE = 0.6           # For neutral signals

# =============================================================================
# ERROR HANDLING
# =============================================================================

ENABLE_MOCK_FALLBACK = True        # Use mock news if API fails
CONTINUE_ON_ERROR = True           # Continue batch processing on errors
ERROR_SENTIMENT = "NEUTRAL"        # Default sentiment on error
ERROR_SCORE = 0                    # Default score on error
ERROR_CONFIDENCE = 0.3             # Default confidence on error

# =============================================================================
# LOGGING & MONITORING
# =============================================================================

VERBOSE_MODE = True                # Print detailed progress messages
SHOW_API_CALLS = True              # Show when API calls are made
SHOW_CACHE_HITS = True             # Show when cache is used
TRACK_TIMING = True                # Track execution time

# Progress indicators
PROGRESS_UPDATE_INTERVAL = 1       # Update every N cryptos
SHOW_EMOJI_INDICATORS = True       # Use emoji in output

# =============================================================================
# CURRENCY MAPPING
# =============================================================================

# Map full names to API symbols
CURRENCY_MAP = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'btc': 'BTC',
    'eth': 'ETH',
    'ripple': 'XRP',
    'cardano': 'ADA',
    'dogecoin': 'DOGE',
    'polkadot': 'DOT',
    'litecoin': 'LTC',
    'chainlink': 'LINK',
    'stellar': 'XLM',
    'uniswap': 'UNI',
    'solana': 'SOL',
    'polygon': 'MATIC',
    'avalanche': 'AVAX'
}

# =============================================================================
# MOCK NEWS DATA (Fallback)
# =============================================================================

MOCK_NEWS_ENABLED = True

MOCK_NEWS = {
    'Bitcoin': [
        {'title': 'Bitcoin shows strong momentum as institutional adoption grows', 
         'source': 'CryptoNews', 'body': 'Market analysis shows positive trends'},
        {'title': 'Major payment processor announces Bitcoin integration', 
         'source': 'FinTech Today', 'body': 'Increasing mainstream adoption'},
        {'title': 'Bitcoin network hash rate reaches new all-time high', 
         'source': 'BlockChain Insights', 'body': 'Network security strengthens'},
    ],
    'Ethereum': [
        {'title': 'Ethereum Layer 2 solutions see record transaction volumes', 
         'source': 'ETH News', 'body': 'Scalability improvements paying off'},
        {'title': 'Major DeFi protocol launches on Ethereum mainnet', 
         'source': 'DeFi Daily', 'body': 'Ecosystem expansion continues'},
        {'title': 'Ethereum staking rewards attract institutional investors', 
         'source': 'Crypto Investor', 'body': 'Growing institutional interest'},
    ]
}

# =============================================================================
# PROMPT TEMPLATES (Optimized)
# =============================================================================

SENTIMENT_PROMPT_TEMPLATE = """Analyze these {crypto_name} news headlines for market sentiment.

Headlines:
{news_summary}

Return ONLY valid JSON:
{{
    "sentiment": "BULLISH" or "BEARISH" or "NEUTRAL",
    "score": <-100 to +100>,
    "confidence": <0 to 1>,
    "key_factors": ["factor1", "factor2"],
    "reasoning": "Brief 1-2 sentence explanation"
}}"""

# =============================================================================
# PERFORMANCE TUNING
# =============================================================================

# API rate limiting
MAX_REQUESTS_PER_MINUTE = 60       # Max API calls per minute
REQUEST_DELAY = 0                  # Delay between requests (seconds)

# Parallel processing (future feature)
ENABLE_PARALLEL_PROCESSING = False # Not implemented yet
MAX_WORKERS = 3                    # Number of parallel workers

# Memory management
MAX_CACHE_SIZE = 1000              # Max cached items per cache type
CLEAR_CACHE_ON_SIZE_LIMIT = False  # Clear oldest when limit reached

# =============================================================================
# VISUALIZATION SETTINGS
# =============================================================================

ENABLE_VISUALIZATION = True        # Generate charts
CHART_DPI = 300                    # Chart resolution
CHART_STYLE = 'seaborn'           # Matplotlib style
SAVE_CHARTS = True                 # Save charts to file
CHART_OUTPUT_FILE = 'sentiment_analysis_results.png'

# Chart colors
COLOR_BULLISH = 'green'
COLOR_BEARISH = 'red'
COLOR_NEUTRAL = 'gray'
COLOR_PALETTE = 'Set2'

# =============================================================================
# FILE PATHS
# =============================================================================

DEFAULT_INPUT_FILE = 'combined_crypto_dataset (1).csv'
DEFAULT_OUTPUT_FILE = 'combined_crypto_dataset_with_sentiment.csv'
CHART_OUTPUT_PATH = './agentic/'

# =============================================================================
# VALIDATION SETTINGS
# =============================================================================

RUN_VALIDATION = True              # Run pre-flight checks
VALIDATE_API_KEY = True            # Test Gemini API key
VALIDATE_MODEL_ACCESS = True       # Test Flash model access
VALIDATE_NEWS_API = True           # Test news API connectivity
FAIL_ON_VALIDATION_ERROR = False   # Continue if validation fails

# Validation timeouts
VALIDATION_TIMEOUT = 5             # Seconds for validation tests
API_TEST_MAX_TOKENS = 100          # Tokens for API test

# =============================================================================
# ADVANCED SETTINGS
# =============================================================================

# LangGraph configuration
LANGGRAPH_RECURSION_LIMIT = 100    # Max recursive calls
LANGGRAPH_CHECKPOINT_ENABLED = False  # State checkpointing (future)

# Sentiment score calculation
SENTIMENT_SCORE_MULTIPLIER = 1.0   # Adjust sensitivity
TECHNICAL_SCORE_MULTIPLIER = 4.0   # Convert pct_change to score

# Signal mapping
SIGNAL_SCORES = {
    'STRONG BUY': lambda pct: min(100, 80 + (pct * 4)),
    'BUY': lambda pct: min(80, 40 + (pct * 4)),
    'SELL': lambda pct: max(-80, -40 + (pct * 4)),
    'STRONG SELL': lambda pct: max(-100, -80 + (pct * 4)),
    'HOLD': lambda pct: pct * 4
}

# =============================================================================
# EXPERIMENTAL FEATURES (Not Active)
# =============================================================================

ENABLE_PERSISTENT_CACHE = False    # Save cache to disk
CACHE_FILE_PATH = './cache.pkl'
ENABLE_ASYNC_PROCESSING = False    # Async API calls
ENABLE_STREAMING = False           # Real-time updates
ENABLE_CUSTOM_MODELS = False       # Support other LLMs

# =============================================================================
# DEBUGGING
# =============================================================================

DEBUG_MODE = False                 # Enable debug output
SAVE_DEBUG_LOGS = False            # Save logs to file
DEBUG_LOG_FILE = 'debug.log'
PRINT_STATE_TRANSITIONS = False    # Print LangGraph state changes
PRINT_API_RESPONSES = False        # Print raw API responses

# =============================================================================
# USAGE NOTES
# =============================================================================

"""
To use this configuration in your notebook:

1. Import at the top of your notebook:
   ```python
   import config
   ```

2. Use configuration values:
   ```python
   agent = CryptoSentimentAgent(gemini_api_key=config.GEMINI_API_KEY)
   ```

3. Override settings as needed:
   ```python
   config.ENABLE_VISUALIZATION = False
   config.VERBOSE_MODE = False
   ```

4. For batch processing:
   ```python
   df, results = analyze_dataset(
       csv_path=config.DEFAULT_INPUT_FILE,
       agent=agent,
       sample_size=config.DEFAULT_SAMPLE_SIZE
   )
   ```
"""
