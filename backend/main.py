from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import state
import agent
import tools


class ChatRequest(BaseModel):
    user_input: str
    session_id: str 

class IngredientRequest(BaseModel):
    ingredient1: str
    ingredient2: str

class ChatResponse(BaseModel):
    response: str
    active_agent: str
    session_id: str
    escalation_required: bool = False

class ConflictCheckResponse(BaseModel):
    ingredient1: str
    ingredient2: str
    safe: bool
    reason: str
    
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
    result = tools.ingredient_search(name)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
    
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
    response_text = agent_response["response"]
    escalated = response_text.lower().startswith("requires escalation:")
    return ChatResponse(response=agent_response["response"], active_agent=agent_response["active_agent"], session_id=session_id, escalation_required=escalated)

@app.get("/profile/{session_id}")
def get_profile(session_id: str):
    return {"session_id": session_id, "profile": state.user_profile, "recommended_products": state.user_recommended_products}

@app.get("/routine/{session_id}")
def get_routine(session_id: str):
    return {"session_id": session_id, "routine": state.user_routine}

@app.post("/ingredient/check-conflict")
async def check_ingredient_conflict(request: IngredientRequest):
    """Check if two ingredients are compatible"""
    result_a = tools.ingredient_search(request.ingredient1)
    result_b = tools.ingredient_search(request.ingredient2)

    print(f"Ingredient A: {result_a}")
    print(f"Ingredient B: {result_b}")

    if "error" in result_a or "error" in result_b:
        return ConflictCheckResponse(
            ingredient1=request.ingredient1,
            ingredient2=request.ingredient2,
            safe=False,
            reason="One or both ingredients not found in the database."
        )
    avoid_a = result_a.get("should_not_combine_with", [])
    avoid_b = result_b.get("should_not_combine_with", [])
    if request.ingredient2.lower() in [x.lower() for x in avoid_a] or request.ingredient1.lower() in [x.lower() for x in avoid_b]:
        return ConflictCheckResponse(
            ingredient1=request.ingredient1,
            ingredient2=request.ingredient2,
            safe=False,
            reason=f"{request.ingredient1} and {request.ingredient2} should not be combined according to ingredient data."
        )
    else:
        return ConflictCheckResponse(
            ingredient1=request.ingredient1,
            ingredient2=request.ingredient2,
            safe=True,
            reason="Ingredients are generally considered safe to use together based on ingredient data."
        )
