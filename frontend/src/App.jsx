import { useRef, useEffect, useState } from 'react'
import './App.css'

const sessionId = 'user-001'
const initialProfile = {
  skinType: '',
  hairType: '',
  concerns: '',
  allergies: '',
  recommendedProducts: '',
  morningRoutine: [],
  eveningRoutine: [],
  products: []
}

function App() {
  const [activeTab, setActiveTab] = useState('home')
  const [messages, setMessages] = useState([
    { sender: 'agent', text: 'Hi! I am a skincare and haircare assistant.' }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [profile, setProfile] = useState(initialProfile)
  const [ingredientQuery, setIngredientQuery] = useState('')
  const [ingredientResult, setIngredientResult] = useState(null)
  const [ingredientLoading, setIngredientLoading] = useState(false)
  const [conflictA, setConflictA] = useState('')
  const [conflictB, setConflictB] = useState('')
  const [conflictResult, setConflictResult] = useState(null)
  const [conflictLoading, setConflictLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const res = await fetch(`http://localhost:8000/profile/${sessionId}`)
      if (!res.ok) return
      const data = await res.json()
      const recommendedProducts = Array.isArray(data.recommended_products)
        ? data.recommended_products
            .map(product => (typeof product === 'string' ? product : product.name || product.title || JSON.stringify(product)))
            .join(', ')
        : typeof data.recommended_products === 'string'
        ? data.recommended_products
        : ''

      setProfile({
        skinType: data.profile.skin_type?.value || '',
        hairType: data.profile.hair_type?.value || '',
        concerns: data.profile.concerns?.value?.join(', ') || '',
        allergies: data.profile.known_allergies?.value?.join(', ') || '',
        recommendedProducts,
        morningRoutine: [],
        eveningRoutine: [],
        products: []
      })
    } catch (error) {
      console.error('Unable to load profile:', error)
    }
  }

  const handleSend = async () => {
    const text = input.trim()
    if (!text) return

    const userMessage = { sender: 'user', text }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_input: text,
          session_id: sessionId
        })
      })
      const data = await res.json()
      const aiMessage = { sender: 'agent', text: data.response || 'Sorry, I did not receive a response.' }
      setMessages(prev => [...prev, aiMessage])
      await fetchProfile()
    } catch (error) {
      console.error('Chat request failed:', error)
      setMessages(prev => [...prev, { sender: 'agent', text: 'There was an error sending your message. Please try again.' }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = event => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSend()
    }
  }

  const handleIngredientLookup = async () => {
    const name = ingredientQuery.trim()
    if (!name) return

    setIngredientLoading(true)
    setIngredientResult(null)
    try {
      const res = await fetch(`http://localhost:8000/ingredient/${encodeURIComponent(name)}`)
      const data = await res.json()
      setIngredientResult(data)
    } catch (error) {
      console.error('Ingredient lookup failed:', error)
      setIngredientResult({ error: 'Unable to load ingredient information.' })
    } finally {
      setIngredientLoading(false)
    }
  }

  const handleConflictCheck = async () => {
    const first = conflictA.trim()
    const second = conflictB.trim()
    if (!first || !second) return

    setConflictLoading(true)
    setConflictResult(null)
    try {
      const res = await fetch('http://localhost:8000/ingredient/check-conflict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ingredient1: first, ingredient2: second })
      })
      const data = await res.json()
      setConflictResult(data)
    } catch (error) {
      console.error('Conflict check failed:', error)
      setConflictResult({ safe: false, message: 'Unable to check conflict. Please try again.' })
    } finally {
      setConflictLoading(false)
    }
  }

  const renderRoutine = (title, icon, message) => (
    <div className="card">
      <div className="card-head">
        <div className="card-icon">{icon}</div>
        <span className="card-title">{title}</span>
      </div>
      <div className="empty-msg">{message}</div>
    </div>
  )

  const renderProfileField = (label, value) => (
    <div className="profile-row">
      <span className="profile-label">{label}</span>
      {value ? <span className="profile-value">{value}</span> : <span className="empty-chip">Not set</span>}
    </div>
  )

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="nav-brand">
          <div>
            <div className="nav-title">Skincare and Haircare Advisor</div>
            <div className="nav-sub">Session: {sessionId}</div>
          </div>
        </div>
        <div className="nav-links">
          <button className={`nav-link ${activeTab === 'home' ? 'active' : ''}`} onClick={() => setActiveTab('home')}>
            Home
          </button>
          <button className={`nav-link ${activeTab === 'chat' ? 'active' : ''}`} onClick={() => setActiveTab('chat')}>
            Chat
          </button>
          <button className={`nav-link ${activeTab === 'ingredient' ? 'active' : ''}`} onClick={() => setActiveTab('ingredient')}>
            Ingredient checker
          </button>
        </div>
      </header>

      <main className="main-content">
        {activeTab === 'home' && (
          <section className="home-screen screen active">
            <div className="grid2">
              <div className="card">
                <div className="card-head">
                  <div className="card-icon user">👤</div>
                  <span className="card-title">Your profile</span>
                </div>
                {renderProfileField('Skin type', profile.skinType)}
                {renderProfileField('Hair type', profile.hairType)}
                {renderProfileField('Concerns', profile.concerns)}
                {renderProfileField('Allergies', profile.allergies)}
              </div>

              <div className="card">
                <div className="card-head">
                  <div className="card-icon heart">💖</div>
                  <span className="card-title">Recommended products</span>
                </div>
                {profile.recommendedProducts ? (
                  <div className="profile-value">{profile.recommendedProducts}</div>
                ) : (
                  <div className="empty-msg">Complete the chat to get personalized product picks.</div>
                )}
              </div>

              <div className="card">
                <div className="card-head">
                  <div className="card-icon sun">☀️</div>
                  <span className="card-title">Morning routine</span>
                </div>
                <div className="empty-msg">Complete the chat to build your morning routine.</div>
              </div>

              <div className="card">
                <div className="card-head">
                  <div className="card-icon moon">🌙</div>
                  <span className="card-title">Evening routine</span>
                </div>
                <div className="empty-msg">Complete the chat to build your evening routine.</div>
              </div>
            </div>
          </section>
        )}

        {activeTab === 'chat' && (
          <section className="screen active">
            <div className="chat-msgs">
              {messages.map((message, index) => (
                <div key={index} className={`msg-row ${message.sender === 'user' ? 'you' : ''}`}>
                  <span className="msg-label">{message.sender === 'user' ? 'You' : 'Advisor'}</span>
                  <div className="bubble">{message.text}</div>
                </div>
              ))}
              {isLoading && (
                <div className="msg-row">
                  <span className="msg-label">Advisor</span>
                  <div className="bubble">Thinking…</div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
            <div className="chat-footer">
              <textarea
                className="chat-input"
                value={input}
                onChange={event => setInput(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type a message…"
              />
              <button className="send-btn" onClick={handleSend} disabled={isLoading}>
                {isLoading ? 'Sending…' : 'Send'}
              </button>
            </div>
          </section>
        )}

        {activeTab === 'ingredient' && (
          <section className="screen active">
            <div className="grid2">
              <div className="card">
                <div className="card-head">
                  <div className="card-icon flask">🧪</div>
                  <span className="card-title">Ingredient lookup</span>
                </div>
                <input
                  className="ing-input"
                  value={ingredientQuery}
                  onChange={event => setIngredientQuery(event.target.value)}
                  placeholder="e.g. niacinamide"
                />
                <button className="ing-btn" onClick={handleIngredientLookup} disabled={ingredientLoading}>
                  {ingredientLoading ? 'Looking up…' : 'Look up'}
                </button>
                {ingredientResult && (
                  <div className="ing-result">
                    <div className="ing-name">{ingredientResult.name || ingredientQuery || 'Ingredient'}</div>
                    <div className="ing-desc">
                      {ingredientResult.description || ingredientResult.error || 'Get ingredient benefits and recommendations here.'}
                    </div>
                  </div>
                )}
              </div>

              <div className="card">
                <div className="card-head">
                  <div className="card-icon refresh">🔄</div>
                  <span className="card-title">Conflict checker</span>
                </div>
                <input
                  className="ing-input"
                  value={conflictA}
                  onChange={event => setConflictA(event.target.value)}
                  placeholder="First ingredient"
                />
                <input
                  className="ing-input"
                  value={conflictB}
                  onChange={event => setConflictB(event.target.value)}
                  placeholder="Second ingredient"
                />
                <button className="ing-btn" onClick={handleConflictCheck} disabled={conflictLoading}>
                  {conflictLoading ? 'Checking…' : 'Check compatibility'}
                </button>
                {conflictResult && (
                  <>
                    <div className={conflictResult.safe ? 'badge-ok' : 'badge-warn'}>
                      {conflictResult.safe ? 'Use with confidence' : 'Use with caution'}
                    </div>
                    <div className="ing-desc">{conflictResult.message || (conflictResult.safe ? 'These ingredients are compatible.' : 'These ingredients may cause irritation together.')}</div>
                  </>
                )}
              </div>
            </div>
          </section>
        )}
      </main>

      <footer className="footer">Yamini Karthik © {new Date().getFullYear()}</footer>
    </div>
  )
}

export default App
