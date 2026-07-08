import os
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, FEW_SHOT_PROMPT
from tools import get_skin_type_info, get_hair_type_info, product_search, ingredient_search
from state import user_profile, user_recommended_products, user_routine

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

#Confidence levels for user profile attributes : "verified", "inferred", "estimated"

def build_case_facts_block() -> str:
    def fmt(field):
        v = user_profile[field]["value"]
        c = user_profile[field]["confidence"]
        if not v:
            return "unknown"
        if isinstance(v, list):
            return f"{', '.join(v)} ({c})" if v else "none stated"
        return f"{v} ({c})"
    
    return f"""
=== USER PROFILE (DO NOT SUMMARIZE OR MODIFY) ===
Skin type: {fmt('skin_type')}
Hair type: {fmt('hair_type')}
Concerns: {fmt('concerns')}
Known allergies: {fmt('known_allergies')}
Price preference: {fmt('price_preference')}
=== END USER PROFILE ===
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=build_case_facts_block() + "\n" + SYSTEM_PROMPT + "\n" + FEW_SHOT_PROMPT,
    tools=[get_skin_type_info, get_hair_type_info, ingredient_search, product_search, update_user_profile, update_recommended_products]
)

def run(message : str, history : list) -> str:
    gemini_history = []
    for turn in history:
        gemini_history.append({"role": turn["role"], "parts": [turn["content"]]})

    chat = model.start_chat(history=gemini_history, enable_automatic_function_calling=True)

    message_with_context = (
        build_case_facts_block() + "\nUser message: " + message)
    response = chat.send_message(message_with_context)
    history.append({"role": "user", "content": message})
    history.append({"role": "model", "content": response.text})
    return response.text

def run_agent():
    print("Skincare/Haircare Advisor")
    print("Type 'quit' to exit\n")


    chat = model.start_chat(enable_automatic_function_calling=True)
    
    while True:
        user_input = input("Enter: ").strip()
        if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
            break
        if not user_input:
            continue
        
        message_with_context = build_case_facts_block() + "\nUser message: " + user_input
        response = chat.send_message(message_with_context)
        if response.text.lower().startswith("requires escalation:"):
            reason = response.text.split(":")[1].strip()
            print(f"\nSkincare/Haircare Advisor: This request requires a professional advice: {reason}")
            print("Please consult a healthcare provider for further assistance.")
        else :
            print(f"\nSkincare/Haircare Advisor: {response.text}")

if __name__ == "__main__":
    run_agent()