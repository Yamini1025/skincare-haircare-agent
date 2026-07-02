import { useEffect, useState } from 'react'
import './App.css'

const sessionId = 'user-001'
const initialProfile = {
  skinType: '',
  hairType: '',
  concerns: '',
  allergies: '',
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

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const res = await fetch(`http://localhost:8000/profile/${sessionId}`)
      if (!res.ok) return
      const data = await res.json()
      setProfile({
        skinType: data.profile.skin_type?.value || '',
        hairType: data.profile.hair_type?.value || '',
        concerns: data.profile.concerns?.value?.join(', ') || '',
        allergies: data.profile.allergies?.value?.join(', ') || '',
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

  const renderRoutine = (title, items) => (
    <div className="card">
      <h2>{title}</h2>
      {items.length ? (
        <ol className="routine-list">
          {items.map((step, index) => (
            <li key={index}>{step}</li>
          ))}
        </ol>
      ) : (
        <p className="placeholder">Complete the chat to build your profile.</p>
      )}
    </div>
  )

  const renderProfileField = (label, value) => (
    <div className="field-row">
      <span>{label}</span>
      <strong>{value || 'Complete the chat to build your profile.'}</strong>
    </div>
  )

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <h1>Skincare and Haircare Advisor</h1>
          <p className="session-label">Session: {sessionId}</p>
        </div>
        <nav className="tab-nav">
          <button className={activeTab === 'home' ? 'tab-button active' : 'tab-button'} onClick={() => setActiveTab('home')}>
            Home
          </button>
          <button className={activeTab === 'chat' ? 'tab-button active' : 'tab-button'} onClick={() => setActiveTab('chat')}>
            Chat
          </button>
          <button className={activeTab === 'ingredient' ? 'tab-button active' : 'tab-button'} onClick={() => setActiveTab('ingredient')}>
            Ingredient Checker
          </button>
        </nav>
      </header>

      <main className="main-content">
        {activeTab === 'home' && (
          <section className="dashboard-view">
            <div className="dashboard-grid">
              <div className="card profile-card">
                <h2>Profile</h2>
                {renderProfileField('Skin type', profile.skinType)}
                {renderProfileField('Hair type', profile.hairType)}
                {renderProfileField('Concerns', profile.concerns)}
                {renderProfileField('Allergies', profile.allergies)}
              </div>
              <div className="card recommended-card">
                <h2>Recommended Products</h2>
                {profile.products.length ? (
                  <div className="product-list">
                    {profile.products.map((item, index) => (
                      <div key={index} className="product-item">
                        <h3>{item.name}</h3>
                        <p>{item.description}</p>
                        <span className="price-range">{item.price_range || 'Price range unavailable'}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="placeholder">Complete the chat to build your profile.</p>
                )}
              </div>
            </div>

            <div className="dashboard-grid two-column">
              {renderRoutine('Morning Routine', profile.morningRoutine)}
              {renderRoutine('Evening Routine', profile.eveningRoutine)}
            </div>
          </section>
        )}

        {activeTab === 'chat' && (
          <section className="chat-view">
            <div className="chat-panel">
              <div className="panel-header">
                <div>
                  <h2>Advisor Chat</h2>
                  <p>Ask about routines, products, and skin or haircare concerns.</p>
                </div>
              </div>

              <div className="message-list">
                {messages.map((message, index) => (
                  <div key={index} className={`message ${message.sender}`}>
                    <span className="message-label">{message.sender === 'user' ? 'You' : 'Advisor'}</span>
                    <p>{message.text}</p>
                  </div>
                ))}
                {isLoading && (
                  <div className="message agent loading">
                    <span className="message-label">Advisor</span>
                    <p>Thinking…</p>
                  </div>
                )}
              </div>

              <div className="composer">
                <textarea
                  value={input}
                  onChange={event => setInput(event.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Type a message..."
                  rows={4}
                />
                <button type="button" onClick={handleSend} disabled={isLoading}>
                  {isLoading ? 'Sending…' : 'Send'}
                </button>
              </div>
            </div>
          </section>
        )}

        {activeTab === 'ingredient' && (
          <section className="ingredient-view">
            <div className="grid-columns">
              <div className="card lookup-card">
                <h2>Ingredient Lookup</h2>
                <p>Search a single ingredient to review benefits and precautions.</p>
                <div className="form-row">
                  <input
                    value={ingredientQuery}
                    onChange={event => setIngredientQuery(event.target.value)}
                    placeholder="Enter ingredient name"
                  />
                  <button type="button" onClick={handleIngredientLookup} disabled={ingredientLoading}>
                    {ingredientLoading ? 'Loading…' : 'Lookup'}
                  </button>
                </div>
                {ingredientResult && (
                  <div className="ingredient-result">
                    {ingredientResult.error ? (
                      <p className="placeholder">{ingredientResult.error}</p>
                    ) : (
                      <>
                        <div className="detail-row">
                          <strong>Benefits</strong>
                          <p>{ingredientResult.benefits || 'No benefits data available.'}</p>
                        </div>
                        <div className="detail-row">
                          <strong>Side effects</strong>
                          <p>{ingredientResult.side_effects || 'No side effects listed.'}</p>
                        </div>
                        <div className="detail-row">
                          <strong>Suited for</strong>
                          <p>{ingredientResult.suited_for || 'No suited for details.'}</p>
                        </div>
                        <div className="detail-row">
                          <strong>Avoid for</strong>
                          <p>{ingredientResult.avoid_for || 'No avoid for details.'}</p>
                        </div>
                      </>
                    )}
                  </div>
                )}
              </div>

              <div className="card conflict-card">
                <h2>Conflict Checker</h2>
                <p>Compare two ingredients for compatibility.</p>
                <div className="form-row">
                  <input
                    value={conflictA}
                    onChange={event => setConflictA(event.target.value)}
                    placeholder="Ingredient A"
                  />
                </div>
                <div className="form-row">
                  <input
                    value={conflictB}
                    onChange={event => setConflictB(event.target.value)}
                    placeholder="Ingredient B"
                  />
                </div>
                <button type="button" onClick={handleConflictCheck} disabled={conflictLoading}>
                  {conflictLoading ? 'Checking…' : 'Check Conflict'}
                </button>
                {conflictResult && (
                  <div className="conflict-result">
                    <span className={conflictResult.safe ? 'badge badge-safe' : 'badge badge-conflict'}>
                      {conflictResult.safe ? 'Safe' : 'Conflict'}
                    </span>
                    <p>{conflictResult.message || (conflictResult.safe ? 'These ingredients are compatible.' : 'These ingredients may conflict.')}</p>
                  </div>
                )}
              </div>
            </div>
          </section>
        )}
      </main>

      <footer className="app-footer">
        Yamini Karthik © {new Date().getFullYear()}
      </footer>
    </div>
  )
}

export default App
