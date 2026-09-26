import React, { useState } from 'react'
import { Lock, Mail, Eye, EyeOff, TrendingUp } from 'lucide-react'

function Login({ onLogin, onRegister }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  // Demo credentials
  const DEMO_EMAIL = 'admin@dataminds.com'
  const DEMO_PASSWORD = 'admin123'

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    // Simulate API call delay
    setTimeout(() => {
      // Check demo credentials
      if (email === DEMO_EMAIL && password === DEMO_PASSWORD) {
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('userEmail', email)
        localStorage.setItem('userName', 'Admin')
        onLogin()
      } else {
        // Check registered users
        const users = JSON.parse(localStorage.getItem('registeredUsers') || '[]')
        const user = users.find(u => u.email === email && u.password === password)
        
        if (user) {
          localStorage.setItem('isAuthenticated', 'true')
          localStorage.setItem('userEmail', email)
          localStorage.setItem('userName', user.name)
          onLogin()
        } else {
          setError('Invalid email or password')
        }
      }
      setLoading(false)
    }, 800)
  }

  const handleDemoLogin = () => {
    setEmail(DEMO_EMAIL)
    setPassword(DEMO_PASSWORD)
  }

  return (
    <div style={styles.container}>
      <div style={styles.loginCard}>
        {/* Logo & Title */}
        <div style={styles.header}>
          <div style={styles.logoContainer}>
            <TrendingUp size={40} color="#3b82f6" />
          </div>
          <h1 style={styles.title}>Data Minds</h1>
          <p style={styles.subtitle}>Crypto Prediction & Analysis Platform</p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} style={styles.form}>
          {/* Email Field */}
          <div style={styles.inputGroup}>
            <label style={styles.label}>Email Address</label>
            <div style={styles.inputWrapper}>
              <Mail size={20} style={styles.inputIcon} />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                style={styles.input}
                required
              />
            </div>
          </div>

          {/* Password Field */}
          <div style={styles.inputGroup}>
            <label style={styles.label}>Password</label>
            <div style={styles.inputWrapper}>
              <Lock size={20} style={styles.inputIcon} />
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                style={styles.input}
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={styles.eyeButton}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div style={styles.error}>
              {error}
            </div>
          )}

          {/* Login Button */}
          <button
            type="submit"
            disabled={loading}
            style={{
              ...styles.loginButton,
              opacity: loading ? 0.7 : 1,
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>

          {/* Demo Credentials */}
          <div style={styles.demoSection}>
            <p style={styles.demoText}>Demo Credentials:</p>
            <button
              type="button"
              onClick={handleDemoLogin}
              style={styles.demoButton}
            >
              Use Demo Account
            </button>
            <div style={styles.credentialsBox}>
              <code style={styles.code}>Email: {DEMO_EMAIL}</code>
              <code style={styles.code}>Password: {DEMO_PASSWORD}</code>
            </div>
          </div>
        </form>

        {/* Register Link */}
        <div style={{ marginTop: '24px', textAlign: 'center' }}>
          <p style={{ color: '#6b7280', fontSize: '14px', margin: 0 }}>
            Pas encore de compte?{' '}
            <button
              onClick={onRegister}
              style={{
                background: 'none',
                border: 'none',
                color: '#667eea',
                fontWeight: '600',
                cursor: 'pointer',
                padding: 0,
                fontSize: '14px',
                textDecoration: 'underline'
              }}
            >
              Créer un compte
            </button>
          </p>
        </div>

        {/* Footer */}
        <div style={styles.footer}>
          <p style={styles.footerText}>
            Powered by XGBoost, Ollama & LangGraph
          </p>
        </div>
      </div>
    </div>
  )
}

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    padding: '20px',
  },
  loginCard: {
    background: 'white',
    borderRadius: '16px',
    boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
    width: '100%',
    maxWidth: '440px',
    padding: '40px',
  },
  header: {
    textAlign: 'center',
    marginBottom: '40px',
  },
  logoContainer: {
    display: 'inline-flex',
    padding: '16px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    borderRadius: '50%',
    marginBottom: '16px',
  },
  title: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#1f2937',
    margin: '0 0 8px 0',
  },
  subtitle: {
    fontSize: '14px',
    color: '#6b7280',
    margin: 0,
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  inputGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  label: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#374151',
  },
  inputWrapper: {
    position: 'relative',
    display: 'flex',
    alignItems: 'center',
  },
  inputIcon: {
    position: 'absolute',
    left: '16px',
    color: '#9ca3af',
  },
  input: {
    width: '100%',
    padding: '12px 16px 12px 48px',
    fontSize: '14px',
    border: '2px solid #e5e7eb',
    borderRadius: '8px',
    outline: 'none',
    transition: 'all 0.2s',
    fontFamily: 'inherit',
  },
  eyeButton: {
    position: 'absolute',
    right: '16px',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    padding: '4px',
    color: '#9ca3af',
    display: 'flex',
    alignItems: 'center',
  },
  error: {
    padding: '12px',
    background: '#fee2e2',
    color: '#dc2626',
    borderRadius: '8px',
    fontSize: '14px',
    textAlign: 'center',
  },
  loginButton: {
    padding: '14px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'transform 0.2s',
    marginTop: '8px',
  },
  demoSection: {
    marginTop: '24px',
    padding: '20px',
    background: '#f9fafb',
    borderRadius: '8px',
    textAlign: 'center',
  },
  demoText: {
    fontSize: '14px',
    color: '#6b7280',
    margin: '0 0 12px 0',
    fontWeight: '600',
  },
  demoButton: {
    padding: '10px 20px',
    background: '#3b82f6',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    marginBottom: '12px',
  },
  credentialsBox: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
    marginTop: '12px',
  },
  code: {
    fontSize: '12px',
    color: '#4b5563',
    background: '#e5e7eb',
    padding: '6px 12px',
    borderRadius: '4px',
    display: 'block',
  },
  footer: {
    marginTop: '32px',
    paddingTop: '24px',
    borderTop: '1px solid #e5e7eb',
    textAlign: 'center',
  },
  footerText: {
    fontSize: '12px',
    color: '#9ca3af',
    margin: 0,
  },
}

export default Login
