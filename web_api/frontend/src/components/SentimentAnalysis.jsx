import React, { useState } from 'react'
import axios from 'axios'
import { Brain, TrendingUp, TrendingDown, Activity, RefreshCw, AlertCircle, Newspaper, Target } from 'lucide-react'

const API_BASE = 'http://127.0.0.1:8001/api/sentiment'

function SentimentAnalysis() {
  const [selectedCrypto, setSelectedCrypto] = useState('Bitcoin')
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Map display names to API keys
  const cryptoKeyMap = {
    'Bitcoin': 'BTC',
    'Ethereum': 'ETH'
  }

  const analyzeSentiment = async () => {
    setLoading(true)
    setError(null)
    setAnalysis(null)
    
    try {
      // Fetch crypto prediction for technical data
      const predResponse = await axios.get('http://127.0.0.1:8001/api/crypto/predictions')
      const cryptoKey = cryptoKeyMap[selectedCrypto]
      const cryptoData = predResponse.data[cryptoKey]
      
      if (!cryptoData) {
        throw new Error(`No prediction data available for ${selectedCrypto}`)
      }

      // Send to sentiment analysis
      const response = await axios.post(`${API_BASE}/analyze`, {
        crypto: selectedCrypto,
        technical: {
          signal: cryptoData.signal,
          pct_change: cryptoData.predicted_change_percent,
          current_price: cryptoData.current_price,
          predicted_price: cryptoData.next_day_prediction,
          rsi: cryptoData.rsi || 50
        }
      })
      
      setAnalysis(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to analyze sentiment')
    } finally {
      setLoading(false)
    }
  }

  const getSignalColor = (signal) => {
    const signalUpper = signal.toUpperCase()
    if (signalUpper.includes('BUY') || signalUpper.includes('STRONG BUY')) return '#10b981'
    if (signalUpper.includes('SELL') || signalUpper.includes('STRONG SELL')) return '#ef4444'
    return '#f59e0b'
  }

  const getSignalIcon = (signal) => {
    const signalUpper = signal.toUpperCase()
    if (signalUpper.includes('BUY')) return <TrendingUp size={24} />
    if (signalUpper.includes('SELL')) return <TrendingDown size={24} />
    return <Activity size={24} />
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(price)
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#10b981'
    if (confidence >= 0.6) return '#f59e0b'
    return '#ef4444'
  }

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h1 className="card-title">
            <Brain size={32} />
            Sentiment Analysis
          </h1>
        </div>

        <div style={{ marginBottom: '2rem' }}>
          <p style={{ color: '#666', marginBottom: '1rem' }}>
            Combines technical analysis with AI-powered sentiment analysis of recent news articles
          </p>
          
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Select Cryptocurrency:
              </label>
              <select 
                value={selectedCrypto}
                onChange={(e) => setSelectedCrypto(e.target.value)}
                style={{ 
                  padding: '0.5rem 1rem',
                  borderRadius: '8px',
                  border: '1px solid #ddd',
                  fontSize: '1rem'
                }}
              >
                <option value="Bitcoin">Bitcoin (BTC)</option>
                <option value="Ethereum">Ethereum (ETH)</option>
              </select>
            </div>
            
            <button 
              className="btn btn-primary" 
              onClick={analyzeSentiment}
              disabled={loading}
              style={{ marginTop: '1.5rem' }}
            >
              {loading ? <div className="spinner"></div> : <Brain size={20} />}
              Analyze Sentiment
            </button>
          </div>
        </div>

        {error && (
          <div className="alert alert-error">
            <AlertCircle size={20} />
            {error}
          </div>
        )}

        {loading && (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            <div className="spinner" style={{ margin: '0 auto' }}></div>
            <p style={{ marginTop: '1rem', color: '#666' }}>
              Analyzing {selectedCrypto} sentiment from recent news...
            </p>
          </div>
        )}

        {analysis && !loading && (
          <div style={{ display: 'grid', gap: '1.5rem' }}>
            
            {/* Header Section */}
            <div style={{ 
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              padding: '1.5rem',
              borderRadius: '12px'
            }}>
              <h2 style={{ margin: 0, marginBottom: '0.5rem' }}>{analysis.crypto}</h2>
              <p style={{ opacity: 0.9, margin: 0 }}>
                Analysis based on {analysis.news_count} recent news articles
              </p>
              <p style={{ opacity: 0.7, margin: 0, marginTop: '0.5rem', fontSize: '0.9rem' }}>
                {new Date(analysis.timestamp).toLocaleString()}
              </p>
            </div>

            {/* Technical Analysis */}
            <div className="card" style={{ background: '#f8fafc' }}>
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                <Activity size={24} />
                Technical Analysis
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
                <div>
                  <p style={{ color: '#666', fontSize: '0.9rem' }}>Current Price</p>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: '0.25rem 0' }}>
                    {formatPrice(analysis.technical.current_price)}
                  </p>
                </div>
                <div>
                  <p style={{ color: '#666', fontSize: '0.9rem' }}>Predicted Price</p>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: '0.25rem 0' }}>
                    {formatPrice(analysis.technical.predicted_price)}
                  </p>
                </div>
                <div>
                  <p style={{ color: '#666', fontSize: '0.9rem' }}>Signal</p>
                  <div style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: '0.5rem',
                    color: getSignalColor(analysis.technical.signal),
                    fontSize: '1.25rem',
                    fontWeight: 'bold',
                    margin: '0.25rem 0'
                  }}>
                    {getSignalIcon(analysis.technical.signal)}
                    {analysis.technical.signal}
                  </div>
                </div>
                <div>
                  <p style={{ color: '#666', fontSize: '0.9rem' }}>Expected Change</p>
                  <p style={{ 
                    fontSize: '1.5rem', 
                    fontWeight: 'bold', 
                    margin: '0.25rem 0',
                    color: analysis.technical.pct_change >= 0 ? '#10b981' : '#ef4444'
                  }}>
                    {analysis.technical.pct_change >= 0 ? '+' : ''}{analysis.technical.pct_change.toFixed(2)}%
                  </p>
                </div>
              </div>
            </div>

            {/* Sentiment Analysis */}
            <div className="card" style={{ background: '#f8fafc' }}>
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                <Newspaper size={24} />
                News Sentiment
              </h3>
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span style={{ fontWeight: 'bold' }}>
                    {analysis.sentiment.sentiment}
                  </span>
                  <span style={{ 
                    color: getConfidenceColor(analysis.sentiment.confidence),
                    fontWeight: 'bold'
                  }}>
                    {(analysis.sentiment.confidence * 100).toFixed(0)}% confidence
                  </span>
                </div>
                <div style={{ 
                  height: '8px', 
                  background: '#e5e7eb', 
                  borderRadius: '4px',
                  overflow: 'hidden'
                }}>
                  <div style={{ 
                    height: '100%',
                    width: `${analysis.sentiment.score * 100}%`,
                    background: analysis.sentiment.score > 0.5 ? '#10b981' : '#ef4444',
                    transition: 'width 0.3s ease'
                  }}></div>
                </div>
                <p style={{ marginTop: '0.5rem', color: '#666', fontSize: '0.9rem' }}>
                  Score: {analysis.sentiment.score.toFixed(2)} / 1.0
                </p>
              </div>
              
              <div style={{ marginTop: '1rem' }}>
                <p style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>Key Factors:</p>
                <ul style={{ margin: 0, paddingLeft: '1.5rem' }}>
                  {analysis.sentiment.key_factors.map((factor, idx) => (
                    <li key={idx} style={{ marginBottom: '0.25rem', color: '#444' }}>{factor}</li>
                  ))}
                </ul>
              </div>

              <div style={{ 
                marginTop: '1rem', 
                padding: '1rem', 
                background: 'white', 
                borderRadius: '8px',
                borderLeft: '4px solid #667eea'
              }}>
                <p style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>Analysis:</p>
                <p style={{ color: '#444', margin: 0, lineHeight: '1.6' }}>
                  {analysis.sentiment.reasoning}
                </p>
              </div>
            </div>

            {/* Combined Signal */}
            <div className="card" style={{ background: '#f8fafc' }}>
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                <Target size={24} />
                Combined Signal Analysis
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
                <div>
                  <p style={{ color: '#666', fontSize: '0.9rem' }}>Technical Weight</p>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: '0.25rem 0' }}>
                    {(analysis.combined_signal.tech_weight * 100).toFixed(0)}%
                  </p>
                  <p style={{ color: '#666', fontSize: '0.9rem' }}>
                    Score: {analysis.combined_signal.technical_score.toFixed(2)}
                  </p>
                </div>
                <div>
                  <p style={{ color: '#666', fontSize: '0.9rem' }}>Sentiment Weight</p>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: '0.25rem 0' }}>
                    {(analysis.combined_signal.sentiment_weight * 100).toFixed(0)}%
                  </p>
                  <p style={{ color: '#666', fontSize: '0.9rem' }}>
                    Score: {analysis.combined_signal.sentiment_score.toFixed(2)}
                  </p>
                </div>
                <div>
                  <p style={{ color: '#666', fontSize: '0.9rem' }}>Combined Score</p>
                  <p style={{ 
                    fontSize: '1.5rem', 
                    fontWeight: 'bold', 
                    margin: '0.25rem 0',
                    color: analysis.combined_signal.combined_score > 0.5 ? '#10b981' : '#ef4444'
                  }}>
                    {analysis.combined_signal.combined_score.toFixed(2)}
                  </p>
                </div>
                <div>
                  <p style={{ color: '#666', fontSize: '0.9rem' }}>Signals Aligned</p>
                  <p style={{ 
                    fontSize: '1.25rem', 
                    fontWeight: 'bold', 
                    margin: '0.25rem 0',
                    color: analysis.combined_signal.signals_aligned ? '#10b981' : '#f59e0b'
                  }}>
                    {analysis.combined_signal.signals_aligned ? '✓ Yes' : '⚠ No'}
                  </p>
                </div>
              </div>
            </div>

            {/* Final Recommendation */}
            <div className="card" style={{ 
              background: analysis.recommendation.aligned 
                ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                : 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
              color: 'white'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
                <div>
                  <h3 style={{ margin: 0, marginBottom: '0.5rem' }}>Final Recommendation</h3>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '2rem', fontWeight: 'bold' }}>
                    {getSignalIcon(analysis.recommendation.action)}
                    {analysis.recommendation.action}
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <p style={{ margin: 0, fontSize: '0.9rem', opacity: 0.9 }}>Confidence</p>
                  <p style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold' }}>
                    {(analysis.recommendation.confidence * 100).toFixed(0)}%
                  </p>
                </div>
              </div>
              
              <div style={{ 
                background: 'rgba(255, 255, 255, 0.2)', 
                padding: '1rem', 
                borderRadius: '8px',
                backdropFilter: 'blur(10px)'
              }}>
                <p style={{ margin: 0, lineHeight: '1.6' }}>
                  {analysis.recommendation.reasoning}
                </p>
              </div>

              {!analysis.recommendation.aligned && (
                <div style={{ 
                  marginTop: '1rem',
                  padding: '0.75rem',
                  background: 'rgba(255, 255, 255, 0.15)',
                  borderRadius: '8px',
                  fontSize: '0.9rem'
                }}>
                  ⚠ Note: Technical and sentiment signals are not aligned. Exercise additional caution.
                </div>
              )}
            </div>

          </div>
        )}
      </div>
    </div>
  )
}

export default SentimentAnalysis
