import React, { useState, useEffect } from 'react'
import { TrendingUp, MessageCircle, Brain, Menu, X, LogOut } from 'lucide-react'
import Login from './components/Login'
import Register from './components/Register'
import CryptoPredictions from './components/CryptoPredictions'
import RAGChat from './components/RAGChat'
import SentimentAnalysis from './components/SentimentAnalysis'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [showRegister, setShowRegister] = useState(false)
  const [activeTab, setActiveTab] = useState('crypto')
  const [menuOpen, setMenuOpen] = useState(false)

  // Check authentication on mount
  useEffect(() => {
    const authStatus = localStorage.getItem('isAuthenticated')
    if (authStatus === 'true') {
      setIsAuthenticated(true)
    }
  }, [])

  const handleLogin = () => {
    setIsAuthenticated(true)
    setShowRegister(false)
  }

  const handleRegister = () => {
    setIsAuthenticated(true)
    setShowRegister(false)
  }

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('userEmail')
    localStorage.removeItem('userName')
    setIsAuthenticated(false)
    setActiveTab('crypto')
    setShowRegister(false)
  }

  // Show register or login page if not authenticated
  if (!isAuthenticated) {
    if (showRegister) {
      return (
        <Register 
          onRegister={handleRegister}
          onBackToLogin={() => setShowRegister(false)}
        />
      )
    }
    return (
      <Login 
        onLogin={handleLogin}
        onRegister={() => setShowRegister(true)}
      />
    )
  }

  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-container">
          <div className="nav-brand">
            <TrendingUp size={28} />
            <span>Data Minds</span>
          </div>

          <div className={`nav-links ${menuOpen ? 'active' : ''}`}>
            <button 
              className={`nav-btn ${activeTab === 'crypto' ? 'active' : ''}`}
              onClick={() => { setActiveTab('crypto'); setMenuOpen(false); }}
            >
              <TrendingUp size={20} />
              <span>Crypto Predictions</span>
            </button>
            <button 
              className={`nav-btn ${activeTab === 'sentiment' ? 'active' : ''}`}
              onClick={() => { setActiveTab('sentiment'); setMenuOpen(false); }}
            >
              <Brain size={20} />
              <span>Sentiment Analysis</span>
            </button>
            <button 
              className={`nav-btn ${activeTab === 'rag' ? 'active' : ''}`}
              onClick={() => { setActiveTab('rag'); setMenuOpen(false); }}
            >
              <MessageCircle size={20} />
              <span>AI Assistant</span>
            </button>
            <button 
              className="nav-btn logout-mobile"
              onClick={() => { handleLogout(); setMenuOpen(false); }}
              style={{
                borderTop: '1px solid rgba(255, 255, 255, 0.1)',
                marginTop: '0.5rem',
                paddingTop: '1rem'
              }}
            >
              <LogOut size={20} />
              <span>Déconnecter</span>
            </button>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginLeft: 'auto' }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              color: 'white',
              fontSize: '0.95rem',
              fontWeight: '500',
              padding: '0.5rem 1rem',
              backgroundColor: 'rgba(255, 255, 255, 0.15)',
              borderRadius: '8px',
              border: '1px solid rgba(255, 255, 255, 0.2)'
            }}>
              <span>Hello, {localStorage.getItem('userName') || 'User'}</span>
            </div>
            <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)}>
              {menuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
            <button 
              className="logout-button"
              onClick={handleLogout}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                padding: '0.6rem 1.2rem',
                backgroundColor: 'rgba(239, 68, 68, 0.9)',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '0.9rem',
                fontWeight: '500',
                transition: 'all 0.2s',
                boxShadow: '0 2px 8px rgba(239, 68, 68, 0.3)'
              }}
              onMouseEnter={(e) => {
                e.target.style.backgroundColor = 'rgba(220, 38, 38, 0.9)'
                e.target.style.boxShadow = '0 4px 12px rgba(239, 68, 68, 0.4)'
                e.target.style.transform = 'translateY(-1px)'
              }}
              onMouseLeave={(e) => {
                e.target.style.backgroundColor = 'rgba(239, 68, 68, 0.9)'
                e.target.style.boxShadow = '0 2px 8px rgba(239, 68, 68, 0.3)'
                e.target.style.transform = 'translateY(0)'
              }}
            >
              <LogOut size={18} />
              Déconnecter
            </button>
          </div>
        </div>
      </nav>

      <main className="main-content">
        {activeTab === 'crypto' && <CryptoPredictions />}
        {activeTab === 'sentiment' && <SentimentAnalysis />}
        {activeTab === 'rag' && <RAGChat />}
      </main>

      <footer className="footer">
        <p>© 2025 Data Minds | Powered by XGBoost, Ollama & LangGraph</p>
      </footer>
    </div>
  )
}

export default App
