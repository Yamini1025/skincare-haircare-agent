from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import agent


class ChatRequest(BaseModel):
    user_input: str
    session_id: str 

class IngredientRequest(BaseModel):
    ingredient1: str
    ingredient2: str
class ChatResponse(BaseModel):
    response: str
    session_id: str
    escalation_required: bool = False
    
app = FastAPI(title="Skincare and Haircare Agent", description="An AI agent that provides skincare and haircare advice.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ingredient/{name}")
def get_ingredient(name: str):
    """Get information about an ingredient"""
    try:
        result = agent.ingredient_search(name)
        if isinstance(result, str) and "not found" in result.lower():
            return {"error": result}, 404
        return result
    except Exception as e:
        return {"error": str(e)}, 500

@app.post("/ingredient/check-conflict")
def check_ingredient_conflict(request: IngredientRequest):
    """Check if two ingredients are compatible"""
    try:
        # Create a prompt for the agent to evaluate ingredient compatibility
        conflict_check = agent.run(
            f"Are {request.ingredient1} and {request.ingredient2} safe to use together in skincare? Provide a yes/no answer with brief explanation.",
            []
        )
        
        # Parse the response to determine if safe
        is_safe = "yes" in conflict_check.lower() or "safe" in conflict_check.lower()
        
        return {
            "ingredient1": request.ingredient1,
            "ingredient2": request.ingredient2,
            "safe": is_safe,
            "reason": conflict_check,
            "recommendation": "You can safely use these ingredients together." if is_safe else "Consider using these ingredients at different times or consult a dermatologist."
        }
    except Exception as e:
        return {"error": str(e)}, 500
    
@app.get("/")
def root():
    return {"status": "success", "message": "Hello, I am a Skincare and Haircare Advisor!"}

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

@app.get("/routine/{session_id}")
def get_routine(session_id: str):
    if session_id not in history:
        return {"error": "Session not found"}
    return {"session_id": session_id, "routine": agent.user_routine}