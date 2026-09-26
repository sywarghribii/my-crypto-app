import React, { useState } from 'react'
import { Eye, EyeOff, Mail, Lock, User, ArrowLeft } from 'lucide-react'

const Register = ({ onRegister, onBackToLogin }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    setError('')

    // Validation
    if (!formData.name || !formData.email || !formData.password || !formData.confirmPassword) {
      setError('Tous les champs sont obligatoires')
      return
    }

    if (formData.password.length < 6) {
      setError('Le mot de passe doit contenir au moins 6 caractères')
      return
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Les mots de passe ne correspondent pas')
      return
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(formData.email)) {
      setError('Email invalide')
      return
    }

    // Check if user already exists
    const users = JSON.parse(localStorage.getItem('registeredUsers') || '[]')
    if (users.some(user => user.email === formData.email)) {
      setError('Un compte existe déjà avec cet email')
      return
    }

    // Register new user
    const newUser = {
      name: formData.name,
      email: formData.email,
      password: formData.password,
      createdAt: new Date().toISOString()
    }

    users.push(newUser)
    localStorage.setItem('registeredUsers', JSON.stringify(users))
    localStorage.setItem('isAuthenticated', 'true')
    localStorage.setItem('userEmail', formData.email)
    localStorage.setItem('userName', formData.name)

    onRegister()
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    setError('')
  }

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '2rem'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '450px',
        background: 'white',
        borderRadius: '20px',
        boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
        overflow: 'hidden'
      }}>
        {/* Header */}
        <div style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          padding: '2rem',
          textAlign: 'center',
          color: 'white'
        }}>
          <button
            onClick={onBackToLogin}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              background: 'rgba(255, 255, 255, 0.2)',
              border: 'none',
              color: 'white',
              padding: '0.5rem 1rem',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '0.9rem',
              marginBottom: '1rem',
              transition: 'all 0.2s'
            }}
            onMouseEnter={(e) => {
              e.target.style.background = 'rgba(255, 255, 255, 0.3)'
            }}
            onMouseLeave={(e) => {
              e.target.style.background = 'rgba(255, 255, 255, 0.2)'
            }}
          >
            <ArrowLeft size={18} />
            Retour à la connexion
          </button>
          <h1 style={{
            margin: '0',
            fontSize: '2rem',
            fontWeight: '700'
          }}>
            Créer un compte
          </h1>
          <p style={{
            margin: '0.5rem 0 0',
            opacity: '0.9',
            fontSize: '0.95rem'
          }}>
            Rejoignez Data Minds
          </p>
        </div>

        {/* Form */}
        <div style={{ padding: '2rem' }}>
          <form onSubmit={handleSubmit}>
            {/* Name Field */}
            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{
                display: 'block',
                marginBottom: '0.5rem',
                color: '#374151',
                fontSize: '0.9rem',
                fontWeight: '500'
              }}>
                Nom complet
              </label>
              <div style={{
                position: 'relative',
                display: 'flex',
                alignItems: 'center'
              }}>
                <User
                  size={20}
                  style={{
                    position: 'absolute',
                    left: '1rem',
                    color: '#9ca3af'
                  }}
                />
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="Entrez votre nom"
                  style={{
                    width: '100%',
                    padding: '0.75rem 1rem 0.75rem 3rem',
                    border: '2px solid #e5e7eb',
                    borderRadius: '10px',
                    fontSize: '1rem',
                    outline: 'none',
                    transition: 'border-color 0.2s',
                    boxSizing: 'border-box'
                  }}
                  onFocus={(e) => e.target.style.borderColor = '#667eea'}
                  onBlur={(e) => e.target.style.borderColor = '#e5e7eb'}
                />
              </div>
            </div>

            {/* Email Field */}
            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{
                display: 'block',
                marginBottom: '0.5rem',
                color: '#374151',
                fontSize: '0.9rem',
                fontWeight: '500'
              }}>
                Email
              </label>
              <div style={{
                position: 'relative',
                display: 'flex',
                alignItems: 'center'
              }}>
                <Mail
                  size={20}
                  style={{
                    position: 'absolute',
                    left: '1rem',
                    color: '#9ca3af'
                  }}
                />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="votre.email@exemple.com"
                  style={{
                    width: '100%',
                    padding: '0.75rem 1rem 0.75rem 3rem',
                    border: '2px solid #e5e7eb',
                    borderRadius: '10px',
                    fontSize: '1rem',
                    outline: 'none',
                    transition: 'border-color 0.2s',
                    boxSizing: 'border-box'
                  }}
                  onFocus={(e) => e.target.style.borderColor = '#667eea'}
                  onBlur={(e) => e.target.style.borderColor = '#e5e7eb'}
                />
              </div>
            </div>

            {/* Password Field */}
            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{
                display: 'block',
                marginBottom: '0.5rem',
                color: '#374151',
                fontSize: '0.9rem',
                fontWeight: '500'
              }}>
                Mot de passe
              </label>
              <div style={{
                position: 'relative',
                display: 'flex',
                alignItems: 'center'
              }}>
                <Lock
                  size={20}
                  style={{
                    position: 'absolute',
                    left: '1rem',
                    color: '#9ca3af'
                  }}
                />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Minimum 6 caractères"
                  style={{
                    width: '100%',
                    padding: '0.75rem 3rem 0.75rem 3rem',
                    border: '2px solid #e5e7eb',
                    borderRadius: '10px',
                    fontSize: '1rem',
                    outline: 'none',
                    transition: 'border-color 0.2s',
                    boxSizing: 'border-box'
                  }}
                  onFocus={(e) => e.target.style.borderColor = '#667eea'}
                  onBlur={(e) => e.target.style.borderColor = '#e5e7eb'}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    position: 'absolute',
                    right: '1rem',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    padding: '0.25rem',
                    display: 'flex',
                    alignItems: 'center',
                    color: '#9ca3af'
                  }}
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            {/* Confirm Password Field */}
            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{
                display: 'block',
                marginBottom: '0.5rem',
                color: '#374151',
                fontSize: '0.9rem',
                fontWeight: '500'
              }}>
                Confirmer le mot de passe
              </label>
              <div style={{
                position: 'relative',
                display: 'flex',
                alignItems: 'center'
              }}>
                <Lock
                  size={20}
                  style={{
                    position: 'absolute',
                    left: '1rem',
                    color: '#9ca3af'
                  }}
                />
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder="Confirmez votre mot de passe"
                  style={{
                    width: '100%',
                    padding: '0.75rem 3rem 0.75rem 3rem',
                    border: '2px solid #e5e7eb',
                    borderRadius: '10px',
                    fontSize: '1rem',
                    outline: 'none',
                    transition: 'border-color 0.2s',
                    boxSizing: 'border-box'
                  }}
                  onFocus={(e) => e.target.style.borderColor = '#667eea'}
                  onBlur={(e) => e.target.style.borderColor = '#e5e7eb'}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  style={{
                    position: 'absolute',
                    right: '1rem',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    padding: '0.25rem',
                    display: 'flex',
                    alignItems: 'center',
                    color: '#9ca3af'
                  }}
                >
                  {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div style={{
                padding: '0.75rem',
                marginBottom: '1rem',
                backgroundColor: '#fee2e2',
                border: '1px solid #fecaca',
                borderRadius: '8px',
                color: '#dc2626',
                fontSize: '0.9rem'
              }}>
                {error}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              style={{
                width: '100%',
                padding: '1rem',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '10px',
                fontSize: '1rem',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'transform 0.2s, box-shadow 0.2s',
                boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)'
              }}
              onMouseEnter={(e) => {
                e.target.style.transform = 'translateY(-2px)'
                e.target.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.5)'
              }}
              onMouseLeave={(e) => {
                e.target.style.transform = 'translateY(0)'
                e.target.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.4)'
              }}
            >
              S'inscrire
            </button>
          </form>

          {/* Login Link */}
          <div style={{
            marginTop: '1.5rem',
            textAlign: 'center',
            color: '#6b7280',
            fontSize: '0.9rem'
          }}>
            Vous avez déjà un compte?{' '}
            <button
              onClick={onBackToLogin}
              style={{
                background: 'none',
                border: 'none',
                color: '#667eea',
                fontWeight: '600',
                cursor: 'pointer',
                padding: '0',
                fontSize: '0.9rem',
                textDecoration: 'underline'
              }}
              onMouseEnter={(e) => e.target.style.color = '#764ba2'}
              onMouseLeave={(e) => e.target.style.color = '#667eea'}
            >
              Se connecter
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Register
