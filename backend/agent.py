import os
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, FEW_SHOT_PROMPT
import state
from tools import get_skin_type_info, get_hair_type_info, update_user_profile, product_search, update_recommended_products, ingredient_search
from agents import run_intake_agent, run_research_agent, run_planner_agent

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def build_profile_context() -> str:
    return f"""
Skin type: {state.user_profile['skin_type']['value'] or 'unknown'} ({state.user_profile['skin_type']['confidence']})
Hair type: {state.user_profile['hair_type']['value'] or 'unknown'} ({state.user_profile['hair_type']['confidence']})
Concerns: {', '.join(state.user_profile['concerns']['value']) or 'none stated'} ({state.user_profile['concerns']['confidence']})
Known allergies: {', '.join(state.user_profile['known_allergies']['value']) or 'none stated'} ({state.user_profile['known_allergies']['confidence']})
Price preference: {state.user_profile['price_preference']['value'] or 'unknown'} ({state.user_profile['price_preference']['confidence']})
"""

def needs_intake(message: str) -> bool: 
    """Check if profile is still incomplete.""" 
    p = state.user_profile 
    return not p['skin_type']['value'] or not p['hair_type']['value'] 

def run(message : str, history : list) -> str:
    profile_context = build_profile_context()
    message_lower = message.lower() 

    if needs_intake(message): 
        return run_intake_agent(message, profile_context) 
    elif any(word in message_lower for word in ['routine', 'schedule', 'morning', 'evening', 'steps']): 
        return run_planner_agent(message, profile_context)
    elif any(word in message_lower for word in ['recommend', 'product', 'suggest', 'what should']):
        return run_research_agent(message, profile_context) 
    else: 
        return run_intake_agent(message, profile_context)
    
if __name__ == "__main__":
    print("Skincare/Haircare Advisor")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("Enter: ").strip()
        if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
            break
        if not user_input:
            continue
        response = run(user_input, history=[])
        print(f"\nSkincare/Haircare Advisor: {response}")