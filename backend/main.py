from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import agent

app = FastAPI(title="Skincare and Haircare Agent", description="An AI agent that provides skincare and haircare advice.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"status": "success", "message": "Hello, I am a Skincare and Haircare Advisor!"}

class ChatRequest(BaseModel):
    user_input: str
    session_id: str 

class ChatResponse(BaseModel):
    response: str
    session_id: str
    escalation_required: bool = False

history = {}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_input = request.user_input
    session_id = request.session_id

    if session_id not in history:
        history[session_id] = []

    agent_response = agent.run(user_input, history[session_id])
    escalated = agent_response.lower().startswith("requires escalation:")
    return ChatResponse(response=agent_response, session_id=session_id, escalation_required=escalated)

@app.get("/profile/{session_id}")
def get_profile(session_id: str):
    if session_id not in history:
        return {"error": "Session not found"}
    return {"session_id": session_id, "profile": agent.user_profile}