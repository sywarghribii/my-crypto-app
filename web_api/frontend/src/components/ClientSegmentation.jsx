import React, { useState } from 'react'
import axios from 'axios'
import { Users, Upload, User, AlertCircle, CheckCircle, FileText } from 'lucide-react'

const API_BASE = 'http://127.0.0.1:8001/api/clients'

function ClientSegmentation() {
  const [activeMode, setActiveMode] = useState('single') // single, batch, csv
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  // Single prediction form
  const [formData, setFormData] = useState({
    age: '',
    income: '',
    spending_score: '',
    years_customer: ''
  })

  // Batch predictions
  const [batchData, setBatchData] = useState([
    { age: '', income: '', spending_score: '', years_customer: '' }
  ])

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleBatchChange = (index, field, value) => {
    const newBatch = [...batchData]
    newBatch[index][field] = value
    setBatchData(newBatch)
  }

  const addBatchRow = () => {
    setBatchData([...batchData, { age: '', income: '', spending_score: '', years_customer: '' }])
  }

  const removeBatchRow = (index) => {
    setBatchData(batchData.filter((_, i) => i !== index))
  }

  const predictSingle = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const response = await axios.post(`${API_BASE}/predict`, {
        age: parseFloat(formData.age),
        income: parseFloat(formData.income),
        spending_score: parseFloat(formData.spending_score),
        years_customer: parseFloat(formData.years_customer)
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction failed')
    } finally {
      setLoading(false)
    }
  }

  const predictBatch = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const clients = batchData.map(client => ({
        age: parseFloat(client.age),
        income: parseFloat(client.income),
        spending_score: parseFloat(client.spending_score),
        years_customer: parseFloat(client.years_customer)
      }))
      const response = await axios.post(`${API_BASE}/predict/batch`, { clients })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Batch prediction failed')
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post(`${API_BASE}/predict/csv`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'CSV upload failed')
    } finally {
      setLoading(false)
    }
  }

  const getSegmentColor = (segment) => {
    const colors = {
      'High Value': '#10b981',
      'Medium Value': '#f59e0b',
      'Low Value': '#ef4444',
      'At Risk': '#dc2626'
    }
    return colors[segment] || '#6b7280'
  }

  const getSegmentBadge = (segment) => (
    <span style={{
      padding: '0.5rem 1rem',
      borderRadius: '8px',
      fontWeight: '600',
      color: 'white',
      background: getSegmentColor(segment)
    }}>
      {segment}
    </span>
  )

  return (
    <div>
      <div className="card">
        <h1 className="card-title">
          <Users size={32} />
          Client Segmentation
        </h1>
        <p style={{ color: '#666', marginTop: '0.5rem' }}>
          Predict customer segments using AI-powered analysis
        </p>
      </div>

      {/* Mode Selection */}
      <div className="card">
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <button 
            className={`btn ${activeMode === 'single' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveMode('single')}
          >
            <User size={20} />
            Single Client
          </button>
          <button 
            className={`btn ${activeMode === 'batch' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveMode('batch')}
          >
            <Users size={20} />
            Batch Prediction
          </button>
          <button 
            className={`btn ${activeMode === 'csv' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveMode('csv')}
          >
            <Upload size={20} />
            Upload CSV
          </button>
        </div>
      </div>

      {error && (
        <div className="alert alert-error">
          <AlertCircle size={20} />
          {error}
        </div>
      )}

      {/* Single Client Form */}
      {activeMode === 'single' && (
        <div className="card">
          <h2 style={{ marginBottom: '1.5rem', fontSize: '1.25rem', fontWeight: '600' }}>
            Enter Client Details
          </h2>
          <div className="grid-2">
            <div className="form-group">
              <label className="form-label">Age</label>
              <input 
                type="number" 
                name="age"
                className="form-input"
                placeholder="e.g., 35"
                value={formData.age}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Annual Income ($)</label>
              <input 
                type="number" 
                name="income"
                className="form-input"
                placeholder="e.g., 75000"
                value={formData.income}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Spending Score (1-100)</label>
              <input 
                type="number" 
                name="spending_score"
                className="form-input"
                placeholder="e.g., 65"
                value={formData.spending_score}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Years as Customer</label>
              <input 
                type="number" 
                name="years_customer"
                className="form-input"
                placeholder="e.g., 3"
                value={formData.years_customer}
                onChange={handleInputChange}
              />
            </div>
          </div>
          <button 
            className="btn btn-primary"
            onClick={predictSingle}
            disabled={loading}
          >
            {loading ? <div className="spinner"></div> : <CheckCircle size={20} />}
            Predict Segment
          </button>
        </div>
      )}

      {/* Batch Prediction */}
      {activeMode === 'batch' && (
        <div className="card">
          <h2 style={{ marginBottom: '1.5rem', fontSize: '1.25rem', fontWeight: '600' }}>
            Batch Prediction ({batchData.length} clients)
          </h2>
          {batchData.map((client, index) => (
            <div key={index} style={{ 
              padding: '1rem', 
              background: '#f9fafb', 
              borderRadius: '8px', 
              marginBottom: '1rem' 
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <span style={{ fontWeight: '600' }}>Client {index + 1}</span>
                {batchData.length > 1 && (
                  <button 
                    className="btn btn-secondary"
                    style={{ padding: '0.25rem 0.75rem', fontSize: '0.875rem' }}
                    onClick={() => removeBatchRow(index)}
                  >
                    Remove
                  </button>
                )}
              </div>
              <div className="grid-2" style={{ gridTemplateColumns: 'repeat(4, 1fr)' }}>
                <input 
                  type="number" 
                  className="form-input"
                  placeholder="Age"
                  value={client.age}
                  onChange={(e) => handleBatchChange(index, 'age', e.target.value)}
                />
                <input 
                  type="number" 
                  className="form-input"
                  placeholder="Income"
                  value={client.income}
                  onChange={(e) => handleBatchChange(index, 'income', e.target.value)}
                />
                <input 
                  type="number" 
                  className="form-input"
                  placeholder="Score"
                  value={client.spending_score}
                  onChange={(e) => handleBatchChange(index, 'spending_score', e.target.value)}
                />
                <input 
                  type="number" 
                  className="form-input"
                  placeholder="Years"
                  value={client.years_customer}
                  onChange={(e) => handleBatchChange(index, 'years_customer', e.target.value)}
                />
              </div>
            </div>
          ))}
          <div style={{ display: 'flex', gap: '1rem' }}>
            <button className="btn btn-secondary" onClick={addBatchRow}>
              + Add Client
            </button>
            <button 
              className="btn btn-primary"
              onClick={predictBatch}
              disabled={loading}
            >
              {loading ? <div className="spinner"></div> : <CheckCircle size={20} />}
              Predict All
            </button>
          </div>
        </div>
      )}

      {/* CSV Upload */}
      {activeMode === 'csv' && (
        <div className="card">
          <h2 style={{ marginBottom: '1.5rem', fontSize: '1.25rem', fontWeight: '600' }}>
            Upload CSV File
          </h2>
          <div style={{ 
            border: '2px dashed #d1d5db', 
            borderRadius: '8px', 
            padding: '2rem', 
            textAlign: 'center',
            background: '#f9fafb'
          }}>
            <FileText size={48} style={{ margin: '0 auto', color: '#9ca3af' }} />
            <p style={{ margin: '1rem 0', color: '#666' }}>
              Upload a CSV file with columns: age, income, spending_score, years_customer
            </p>
            <input 
              type="file" 
              accept=".csv"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
              id="csv-upload"
            />
            <label htmlFor="csv-upload" className="btn btn-primary" style={{ cursor: 'pointer' }}>
              <Upload size={20} />
              Choose CSV File
            </label>
          </div>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="card">
          <h2 className="card-title">
            <CheckCircle size={24} />
            Prediction Results
          </h2>

          {result.segment && (
            // Single prediction result
            <div>
              <div style={{ 
                padding: '2rem', 
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                borderRadius: '12px',
                color: 'white',
                marginBottom: '1.5rem'
              }}>
                <div style={{ fontSize: '1rem', opacity: 0.9, marginBottom: '0.5rem' }}>
                  Predicted Segment
                </div>
                <div style={{ fontSize: '2.5rem', fontWeight: '700' }}>
                  {result.segment}
                </div>
                <div style={{ fontSize: '1rem', opacity: 0.9, marginTop: '0.5rem' }}>
                  Confidence: {(result.confidence * 100).toFixed(1)}%
                </div>
              </div>

              {result.recommendations && result.recommendations.length > 0 && (
                <div>
                  <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', fontWeight: '600' }}>
                    Recommendations
                  </h3>
                  <ul style={{ listStyle: 'none', padding: 0 }}>
                    {result.recommendations.map((rec, idx) => (
                      <li key={idx} style={{ 
                        padding: '1rem', 
                        background: '#f0fdf4', 
                        borderRadius: '8px', 
                        marginBottom: '0.5rem',
                        borderLeft: '4px solid #10b981'
                      }}>
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {result.predictions && (
            // Batch or CSV results
            <div>
              <p style={{ marginBottom: '1rem', color: '#666' }}>
                Processed {result.predictions.length} clients
              </p>
              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ background: '#f9fafb', borderBottom: '2px solid #e5e7eb' }}>
                      <th style={{ padding: '1rem', textAlign: 'left' }}>Client</th>
                      <th style={{ padding: '1rem', textAlign: 'left' }}>Age</th>
                      <th style={{ padding: '1rem', textAlign: 'left' }}>Income</th>
                      <th style={{ padding: '1rem', textAlign: 'left' }}>Score</th>
                      <th style={{ padding: '1rem', textAlign: 'left' }}>Years</th>
                      <th style={{ padding: '1rem', textAlign: 'left' }}>Segment</th>
                      <th style={{ padding: '1rem', textAlign: 'left' }}>Confidence</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.predictions.map((pred, idx) => (
                      <tr key={idx} style={{ borderBottom: '1px solid #e5e7eb' }}>
                        <td style={{ padding: '1rem' }}>{idx + 1}</td>
                        <td style={{ padding: '1rem' }}>{pred.input.age}</td>
                        <td style={{ padding: '1rem' }}>${pred.input.income.toLocaleString()}</td>
                        <td style={{ padding: '1rem' }}>{pred.input.spending_score}</td>
                        <td style={{ padding: '1rem' }}>{pred.input.years_customer}</td>
                        <td style={{ padding: '1rem' }}>{getSegmentBadge(pred.segment)}</td>
                        <td style={{ padding: '1rem' }}>{(pred.confidence * 100).toFixed(1)}%</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ClientSegmentation
