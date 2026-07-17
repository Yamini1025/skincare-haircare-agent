import { useRef, useEffect, useState } from 'react'
import './App.css'

const sessionId = 'user-001'
const initialProfile = {
  skinType: '',
  hairType: '',
  concerns: '',
  allergies: '',
  recommendedProducts: '',
  skin_am_routine: [],
  skin_pm_routine: [],
  hair_am_routine: [],
  hair_pm_routine: [],
  products: []
}

function App() {
  const [activeTab, setActiveTab] = useState('home')
  const [messages, setMessages] = useState([
    { sender: 'agent', text: 'Hi! I am a skincare and haircare assistant.' }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [activeAgent, setActiveAgent] = useState('Advisor')
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
      const profileRes = await fetch(`http://localhost:8000/profile/${sessionId}`)
      const routineRes = await fetch(`http://localhost:8000/routine/${sessionId}`)
      if (!profileRes.ok) return
      const data = await profileRes.json()
      const recommendedProducts = Array.isArray(data.recommended_products)
        ? data.recommended_products
            .map(product => (typeof product === 'string' ? product : product.name || product.title || JSON.stringify(product)))
            .join(', ')
        : typeof data.recommended_products === 'string'
        ? data.recommended_products
        : ''

        const routineData = routineRes.ok ? await routineRes.json() : {}

      setProfile({
        skinType: data.profile.skin_type?.value || '',
        hairType: data.profile.hair_type?.value || '',
        concerns: data.profile.concerns?.value?.join(', ') || '',
        allergies: data.profile.known_allergies?.value?.join(', ') || '',
        recommendedProducts,

        skin_am_routine: routineData.routine?.skin_am || [],
        skin_pm_routine: routineData.routine?.skin_pm || [],
        hair_am_routine: routineData.routine?.hair_am || [],
        hair_pm_routine: routineData.routine?.hair_pm || [],
        products: routineData.routine?.products || []
      })
    } catch (error) {
      console.error('Unable to load profile:', error)
    }
  }

  const handleSend = async () => {
    const text = input.trim()
    if (!text) return

    const lower = text.toLowerCase()

      const recommendationKeywords = [
        'recommend',
        'suggest',
        'routine',
        'morning',
        'evening',
        'product',
        'products',
        'ingredient',
        'ingredients',
        'use',
        'apply',
        'cleanser',
        'moisturizer',
        'serum',
        'sunscreen',
        'shampoo',
        'conditioner',
        'mask'
      ]

      setActiveAgent(
        recommendationKeywords.some(word => lower.includes(word))
          ? 'Recommendation Agent'
          : 'Intake Agent'
      )

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
      setActiveAgent(data.active_agent)
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

  const renderRoutineColumn = (items) => (
    <>
      {items.map((item, index) => (
        <div key={index} className="routine-item">
          {item}
        </div>
      ))}
    </>
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
                <div className="routine-split">
                  <div className="routine-column">
                    <div className="column-label">Skin:</div>
                    {profile.skin_am_routine.length > 0 ? (
                      renderRoutineColumn(profile.skin_am_routine)
                    ) : (
                      <div className="empty-msg">No skin steps yet.</div>
                    )}
                  </div>
                  <div className="routine-divider"></div>
                  <div className="routine-column">
                    <div className="column-label">Hair:</div>
                    {profile.hair_am_routine.length > 0 ? (
                      renderRoutineColumn(profile.hair_am_routine)
                    ) : (
                      <div className="empty-msg">No hair steps yet.</div>
                    )}
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="card-head">
                  <div className="card-icon moon">🌙</div>
                  <span className="card-title">Evening routine</span>
                </div>
                <div className="routine-split">
                  <div className="routine-column">
                    <div className="column-label">Skin:</div>
                    {profile.skin_pm_routine.length > 0 ? (
                      renderRoutineColumn(profile.skin_pm_routine)
                    ) : (
                      <div className="empty-msg">No skin steps yet.</div>
                    )}
                  </div>
                  <div className="routine-divider"></div>
                  <div className="routine-column">
                    <div className="column-label">Hair:</div>
                    {profile.hair_pm_routine.length > 0 ? (
                      renderRoutineColumn(profile.hair_pm_routine)
                    ) : (
                      <div className="empty-msg">No hair steps yet.</div>
                    )}
                  </div>
                </div>
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
                  <div className="bubble">{activeAgent} is working...</div>
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
                    <div className="ing-name">{ingredientQuery}</div>
                    {ingredientResult.error ? (
                      <div className="ing-desc">{ingredientResult.error}</div>
                    ) : (
                      <>
                        {ingredientResult.benefits && (
                          <div className="detail-row">
                            <strong>Benefits</strong>
                            <ul>{ingredientResult.benefits.map((b, i) => <li key={i}>{b}</li>)}</ul>
                          </div>
                        )}
                        {ingredientResult.suitable_for && (
                          <div className="detail-row">
                            <strong>Suited for</strong>
                            <p>{ingredientResult.suitable_for.join(', ')}</p>
                          </div>
                        )}
                        {ingredientResult.avoid_for && (
                          <div className="detail-row">
                            <strong>Avoid for</strong>
                            <p>{ingredientResult.avoid_for.join(', ')}</p>
                          </div>
                        )}
                        {ingredientResult.should_not_combine_with && (
                          <div className="detail-row">
                            <strong>Don't combine with</strong>
                            <p>{ingredientResult.should_not_combine_with.join(', ')}</p>
                          </div>
                        )}
                        {ingredientResult.potential_side_effects && (
                          <div className="detail-row">
                            <strong>Side effects</strong>
                            <p>{ingredientResult.potential_side_effects.join(', ')}</p>
                          </div>
                        )}
                      </>
                    )}
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
                    <div className="ing-desc">{conflictResult.reason || (conflictResult.safe ? 'These ingredients are compatible.' : 'These ingredients may cause irritation together.')}</div>
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
