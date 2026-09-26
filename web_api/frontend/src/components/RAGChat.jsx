import React, { useState, useRef, useEffect } from 'react'
import { MessageCircle, Send, Trash2, Info, Clock, FileText, Loader } from 'lucide-react'

const RAGChat = () => {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8001/api/rag/stats')
      const data = await response.json()
      setStats(data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const userMessage = {
      type: 'user',
      content: input,
      timestamp: new Date().toLocaleTimeString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch('http://127.0.0.1:8001/api/rag/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input, use_history: true })
      })

      const data = await response.json()

      const botMessage = {
        type: 'bot',
        content: data.answer,
        sources: data.sources || [],
        confidence: data.confidence,
        metrics: data.metrics || {
          search_time: 0,
          generation_time: 0,
          total_time: 0,
          num_sources: 0
        },
        timestamp: new Date().toLocaleTimeString()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage = {
        type: 'error',
        content: `Error: ${error.message}`,
        timestamp: new Date().toLocaleTimeString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const clearHistory = async () => {
    try {
      await fetch('http://127.0.0.1:8001/api/rag/chat/clear', { method: 'POST' })
      setMessages([])
      fetchStats()
    } catch (error) {
      console.error('Error clearing history:', error)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const exampleQuestions = [
    "What is Bitcoin's current prediction?",
    "Explain what RSI and MACD indicators mean",
    "How does the XGBoost model work?",
    "What features are most important for predictions?"
  ]

  return (
    <div className="rag-container">
      {/* Header */}
      <div className="rag-header">
        <div className="rag-title">
          <MessageCircle size={32} />
          <div>
            <h1>Crypto Trading Assistant</h1>
            <p>Ask questions about your crypto prediction models</p>
          </div>
        </div>
        
        {stats && (
          <div className="rag-stats">
            <div className="stat-item">
              <FileText size={16} />
              <span>{stats.total_documents} docs</span>
            </div>
            <div className="stat-item">
              <MessageCircle size={16} />
              <span>{stats.chat_history_length} history</span>
            </div>
            <button className="clear-btn" onClick={clearHistory} title="Clear chat history">
              <Trash2 size={18} />
            </button>
          </div>
        )}
      </div>

      {/* Messages */}
      <div className="rag-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <MessageCircle size={48} className="welcome-icon" />
            <h2>Welcome to the RAG Assistant!</h2>
            <p>I can answer questions about your crypto prediction models, technical indicators, and trading strategies.</p>
            
            <div className="example-questions">
              <h3>Try asking:</h3>
              {exampleQuestions.map((q, idx) => (
                <button 
                  key={idx}
                  className="example-btn"
                  onClick={() => setInput(q)}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.type}`}>
            <div className="message-content">
              {msg.content}
            </div>
            
            {msg.sources && msg.sources.length > 0 && (
              <div className="message-sources">
                <strong>📚 Sources:</strong>
                <ul>
                  {msg.sources.map((source, i) => (
                    <li key={i}>
                      <div className="source-content">{source.content}</div>
                      <div className="source-relevance">Relevance: {(source.relevance * 100).toFixed(0)}%</div>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {msg.metrics && (
              <div className="message-metrics">
                <span>⚡ {msg.metrics.total_time}s total</span>
                <span>🔍 {msg.metrics.search_time}s search</span>
                <span>🤖 {msg.metrics.generation_time}s generation</span>
                <span>📚 {msg.metrics.num_sources} sources</span>
                <span>📊 {(msg.confidence * 100).toFixed(0)}% confidence</span>
                <span className="timestamp">{msg.timestamp}</span>
              </div>
            )}
            
            {msg.type === 'user' && (
              <div className="timestamp">{msg.timestamp}</div>
            )}
          </div>
        ))}

        {loading && (
          <div className="message bot loading-message">
            <Loader className="spinner" size={20} />
            <span>Thinking...</span>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="rag-input">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about crypto predictions, models, indicators..."
          rows={3}
          disabled={loading}
        />
        <button 
          onClick={sendMessage} 
          disabled={!input.trim() || loading}
          className="send-btn"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  )
}

export default RAGChat
