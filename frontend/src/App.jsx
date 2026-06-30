import { useState } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([
    { sender: 'agent', text: 'Hi! I am a skincare and haircare assistant.' }
  ])
  const [input, setInput] = useState('')
  const sessionId = 'user-001'

  const handleSend = async () => {
    if (!input.trim()) return
    const text = input
    const userMessage = { sender: "user", text }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_input: text,
      session_id: sessionId
    })
    })
    const data = await res.json()
    const aiMessage = {
    sender: "agent",
    text: data.response
    }

    setMessages(prev => [...prev, aiMessage])
  }

  const handleKeyDown = event => {
    if (event.key === 'Enter') {
      event.preventDefault()
      handleSend()
    }
  }

  return (
    <main className="app-shell">
      <section className="chat-panel">
        <div className="panel-header">
          <div>
            <h1>Skincare & Haircare Chat</h1>
            <p>Session: {sessionId}</p>
          </div>
        </div>

        <div className="message-list">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <span className="message-label">
                {message.sender === 'user' ? 'You' : 'Agent'}
              </span>
              <p>{message.text}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="input-panel">
        <div className="input-panel-inner">
          <h2>Send a message</h2>
          <textarea
            value={input}
            onChange={event => setInput(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your question here..."
            rows={6}
          />
          <button type="button" onClick={handleSend}>
            Send
          </button>
        </div>
      </section>
    </main>
  )
}

export default App
