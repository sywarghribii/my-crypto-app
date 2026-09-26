import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TrendingUp, RefreshCw, DollarSign, AlertCircle, Activity } from 'lucide-react'

const API_BASE = 'http://127.0.0.1:8001/api/crypto'

function CryptoPredictions() {
  const [predictions, setPredictions] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [lastUpdate, setLastUpdate] = useState(null)

  useEffect(() => {
    fetchPredictions()
  }, [])

  const fetchPredictions = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_BASE}/predictions`)
      setPredictions(response.data)
      setLastUpdate(new Date().toLocaleTimeString())
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch predictions')
    } finally {
      setLoading(false)
    }
  }

  const refreshPredictions = async () => {
    setLoading(true)
    setError(null)
    try {
      await axios.post(`${API_BASE}/predictions/refresh`)
      await fetchPredictions()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to refresh predictions')
      setLoading(false)
    }
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(price)
  }

  const getChangeColor = (change) => {
    return change >= 0 ? '#10b981' : '#ef4444'
  }

  const getChangeIcon = (change) => {
    return change >= 0 ? '↑' : '↓'
  }

  if (loading && !predictions) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '4rem' }}>
        <div className="spinner" style={{ margin: '0 auto' }}></div>
        <p style={{ marginTop: '1rem', color: '#666' }}>Loading predictions...</p>
      </div>
    )
  }

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h1 className="card-title">
            <TrendingUp size={32} />
            Cryptocurrency Price Predictions
          </h1>
          <button 
            className="btn btn-primary" 
            onClick={refreshPredictions}
            disabled={loading}
          >
            {loading ? <div className="spinner"></div> : <RefreshCw size={20} />}
            Refresh Data
          </button>
        </div>

        {error && (
          <div className="alert alert-error">
            <AlertCircle size={20} />
            {error}
          </div>
        )}

        {lastUpdate && (
          <p style={{ color: '#666', marginBottom: '1rem' }}>
            Last updated: {lastUpdate}
          </p>
        )}
      </div>

      {predictions && (
        <>
          <div className="grid-2">
            {/* Bitcoin Card */}
            <div className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <div>
                  <h2 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#666', marginBottom: '0.5rem' }}>
                    Bitcoin (BTC)
                  </h2>
                  <div style={{ fontSize: '2rem', fontWeight: '700', color: '#333' }}>
                    {formatPrice(predictions.BTC.current_price)}
                  </div>
                </div>
                <div style={{ 
                  padding: '1rem', 
                  borderRadius: '12px', 
                  background: 'linear-gradient(135deg, #f7931a 0%, #f7931a 100%)',
                  color: 'white',
                  fontSize: '2rem'
                }}>
                  ₿
                </div>
              </div>

              <div style={{ borderTop: '1px solid #e0e0e0', paddingTop: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span style={{ color: '#666' }}>Next Day Prediction</span>
                  <span style={{ fontWeight: '700', color: '#333' }}>
                    {formatPrice(predictions.BTC.next_day_prediction)}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span style={{ color: '#666' }}>Expected Change</span>
                  <span style={{ fontWeight: '700', color: getChangeColor(predictions.BTC.predicted_change_percent) }}>
                    {getChangeIcon(predictions.BTC.predicted_change_percent)} {Math.abs(predictions.BTC.predicted_change_percent).toFixed(2)}%
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#666' }}>Change Amount</span>
                  <span style={{ fontWeight: '700', color: getChangeColor(predictions.BTC.predicted_change_amount) }}>
                    {formatPrice(predictions.BTC.predicted_change_amount)}
                  </span>
                </div>
              </div>

              <div style={{ 
                marginTop: '1rem', 
                padding: '1rem', 
                borderRadius: '8px', 
                background: predictions.BTC.trend === 'up' ? '#f0fdf4' : '#fef2f2'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <Activity size={16} />
                  <span style={{ fontWeight: '600' }}>Market Sentiment</span>
                </div>
                <p style={{ color: '#666', fontSize: '0.9rem' }}>
                  {predictions.BTC.recommendation}
                </p>
              </div>
            </div>

            {/* Ethereum Card */}
            <div className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <div>
                  <h2 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#666', marginBottom: '0.5rem' }}>
                    Ethereum (ETH)
                  </h2>
                  <div style={{ fontSize: '2rem', fontWeight: '700', color: '#333' }}>
                    {formatPrice(predictions.ETH.current_price)}
                  </div>
                </div>
                <div style={{ 
                  padding: '1rem', 
                  borderRadius: '12px', 
                  background: 'linear-gradient(135deg, #627eea 0%, #8e44ad 100%)',
                  color: 'white',
                  fontSize: '2rem'
                }}>
                  Ξ
                </div>
              </div>

              <div style={{ borderTop: '1px solid #e0e0e0', paddingTop: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span style={{ color: '#666' }}>Next Day Prediction</span>
                  <span style={{ fontWeight: '700', color: '#333' }}>
                    {formatPrice(predictions.ETH.next_day_prediction)}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span style={{ color: '#666' }}>Expected Change</span>
                  <span style={{ fontWeight: '700', color: getChangeColor(predictions.ETH.predicted_change_percent) }}>
                    {getChangeIcon(predictions.ETH.predicted_change_percent)} {Math.abs(predictions.ETH.predicted_change_percent).toFixed(2)}%
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#666' }}>Change Amount</span>
                  <span style={{ fontWeight: '700', color: getChangeColor(predictions.ETH.predicted_change_amount) }}>
                    {formatPrice(predictions.ETH.predicted_change_amount)}
                  </span>
                </div>
              </div>

              <div style={{ 
                marginTop: '1rem', 
                padding: '1rem', 
                borderRadius: '8px', 
                background: predictions.ETH.trend === 'up' ? '#f0fdf4' : '#fef2f2'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <Activity size={16} />
                  <span style={{ fontWeight: '600' }}>Market Sentiment</span>
                </div>
                <p style={{ color: '#666', fontSize: '0.9rem' }}>
                  {predictions.ETH.recommendation}
                </p>
              </div>
            </div>
          </div>

          {/* Statistics Dashboard */}
          <div className="grid-3">
            <div className="card" style={{ textAlign: 'center', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
              <Activity size={32} style={{ margin: '0 auto 1rem' }} />
              <div style={{ fontSize: '2rem', fontWeight: '700', marginBottom: '0.5rem' }}>
                {((predictions.BTC.confidence + predictions.ETH.confidence) / 2 * 100).toFixed(1)}%
              </div>
              <div style={{ opacity: 0.9 }}>Average Confidence</div>
            </div>
            
            <div className="card" style={{ textAlign: 'center', background: predictions.BTC.trend === 'up' ? '#10b981' : predictions.BTC.trend === 'down' ? '#ef4444' : '#f59e0b', color: 'white' }}>
              <TrendingUp size={32} style={{ margin: '0 auto 1rem' }} />
              <div style={{ fontSize: '2rem', fontWeight: '700', marginBottom: '0.5rem' }}>
                {predictions.BTC.signal}
              </div>
              <div style={{ opacity: 0.9 }}>Bitcoin Signal</div>
            </div>
            
            <div className="card" style={{ textAlign: 'center', background: predictions.ETH.trend === 'up' ? '#10b981' : predictions.ETH.trend === 'down' ? '#ef4444' : '#f59e0b', color: 'white' }}>
              <TrendingUp size={32} style={{ margin: '0 auto 1rem' }} />
              <div style={{ fontSize: '2rem', fontWeight: '700', marginBottom: '0.5rem' }}>
                {predictions.ETH.signal}
              </div>
              <div style={{ opacity: 0.9 }}>Ethereum Signal</div>
            </div>
          </div>

          {/* Price Charts */}
          <div className="grid-2">
            <div className="card">
              <h2 className="card-title" style={{ color: '#f7931a' }}>
                <DollarSign size={24} />
                Bitcoin Price Trend
              </h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={[
                  { 
                    date: 'Today', 
                    price: predictions.BTC.current_price,
                    label: `Current: ${formatPrice(predictions.BTC.current_price)}`
                  },
                  { 
                    date: 'Tomorrow', 
                    price: predictions.BTC.next_day_prediction,
                    label: `Predicted: ${formatPrice(predictions.BTC.next_day_prediction)}`
                  }
                ]}
                margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                  <XAxis 
                    dataKey="date" 
                    stroke="#666"
                    style={{ fontSize: '0.875rem', fontWeight: '600' }}
                  />
                  <YAxis 
                    stroke="#666"
                    style={{ fontSize: '0.875rem' }}
                    domain={[
                      Math.floor(Math.min(predictions.BTC.current_price, predictions.BTC.next_day_prediction) * 0.995),
                      Math.ceil(Math.max(predictions.BTC.current_price, predictions.BTC.next_day_prediction) * 1.005)
                    ]}
                    tickFormatter={(value) => `$${(value / 1000).toFixed(1)}k`}
                  />
                  <Tooltip 
                    formatter={(value) => formatPrice(value)}
                    contentStyle={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px' }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="price" 
                    stroke="#f7931a" 
                    strokeWidth={4}
                    dot={{ fill: '#f7931a', r: 8 }}
                    activeDot={{ r: 10 }}
                  />
                </LineChart>
              </ResponsiveContainer>
              <div style={{ marginTop: '1rem', padding: '1rem', background: '#fff8f0', borderRadius: '8px', borderLeft: '4px solid #f7931a' }}>
                <strong>Change: </strong>
                <span style={{ color: getChangeColor(predictions.BTC.predicted_change_percent) }}>
                  {getChangeIcon(predictions.BTC.predicted_change_percent)} {formatPrice(Math.abs(predictions.BTC.predicted_change_amount))} 
                  ({Math.abs(predictions.BTC.predicted_change_percent).toFixed(2)}%)
                </span>
              </div>
            </div>

            <div className="card">
              <h2 className="card-title" style={{ color: '#627eea' }}>
                <DollarSign size={24} />
                Ethereum Price Trend
              </h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={[
                  { 
                    date: 'Today', 
                    price: predictions.ETH.current_price,
                    label: `Current: ${formatPrice(predictions.ETH.current_price)}`
                  },
                  { 
                    date: 'Tomorrow', 
                    price: predictions.ETH.next_day_prediction,
                    label: `Predicted: ${formatPrice(predictions.ETH.next_day_prediction)}`
                  }
                ]}
                margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                  <XAxis 
                    dataKey="date" 
                    stroke="#666"
                    style={{ fontSize: '0.875rem', fontWeight: '600' }}
                  />
                  <YAxis 
                    stroke="#666"
                    style={{ fontSize: '0.875rem' }}
                    domain={[
                      Math.floor(Math.min(predictions.ETH.current_price, predictions.ETH.next_day_prediction) * 0.995),
                      Math.ceil(Math.max(predictions.ETH.current_price, predictions.ETH.next_day_prediction) * 1.005)
                    ]}
                    tickFormatter={(value) => `$${(value / 1000).toFixed(1)}k`}
                  />
                  <Tooltip 
                    formatter={(value) => formatPrice(value)}
                    contentStyle={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px' }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="price" 
                    stroke="#627eea" 
                    strokeWidth={4}
                    dot={{ fill: '#627eea', r: 8 }}
                    activeDot={{ r: 10 }}
                  />
                </LineChart>
              </ResponsiveContainer>
              <div style={{ marginTop: '1rem', padding: '1rem', background: '#f0f4ff', borderRadius: '8px', borderLeft: '4px solid #627eea' }}>
                <strong>Change: </strong>
                <span style={{ color: getChangeColor(predictions.ETH.predicted_change_percent) }}>
                  {getChangeIcon(predictions.ETH.predicted_change_percent)} {formatPrice(Math.abs(predictions.ETH.predicted_change_amount))} 
                  ({Math.abs(predictions.ETH.predicted_change_percent).toFixed(2)}%)
                </span>
              </div>
            </div>
          </div>

          {/* Market Overview */}
          <div className="card">
            <h2 className="card-title">
              <Activity size={24} />
              Market Overview
            </h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
              <div style={{ padding: '1.5rem', background: '#f9fafb', borderRadius: '12px', border: '2px solid #e5e7eb' }}>
                <div style={{ fontSize: '0.875rem', color: '#666', marginBottom: '0.5rem' }}>BTC Market Cap Impact</div>
                <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#f7931a' }}>
                  {formatPrice(predictions.BTC.current_price * 19500000)} {/* Approximate BTC supply */}
                </div>
              </div>
              <div style={{ padding: '1.5rem', background: '#f9fafb', borderRadius: '12px', border: '2px solid #e5e7eb' }}>
                <div style={{ fontSize: '0.875rem', color: '#666', marginBottom: '0.5rem' }}>ETH Market Cap Impact</div>
                <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#627eea' }}>
                  {formatPrice(predictions.ETH.current_price * 120000000)} {/* Approximate ETH supply */}
                </div>
              </div>
              <div style={{ padding: '1.5rem', background: '#f9fafb', borderRadius: '12px', border: '2px solid #e5e7eb' }}>
                <div style={{ fontSize: '0.875rem', color: '#666', marginBottom: '0.5rem' }}>Prediction Date</div>
                <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#333' }}>
                  {new Date(predictions.BTC.timestamp).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default CryptoPredictions
