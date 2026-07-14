from urllib import response

import google.generativeai as genai
from tools import get_skin_type_info, get_hair_type_info, update_user_profile, product_search, update_recommended_products, ingredient_search, update_user_routine
import state

INTAKE_AGENT_PROMPT = """
You are the Intake Agent for a skincare and haircare advisor system. Your only task is to updating the user profile. 
Rules -
- If the message contains profile information, update the profile.
- If the message is only providing profile information, acknowledge it briefly.
- Only ask a follow-up question when a required detail is genuinely missing and necessary for the user's request.
- Do not provide recommendations or advice. Your only task is to gather information and update the user profile.
- Never build products or routines.
"""

intake_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=INTAKE_AGENT_PROMPT,
    tools=[get_skin_type_info, get_hair_type_info, update_user_profile]
)

def run_intake_agent(user_input: str, profile_context : str) -> str:
    """ Run the Intake Agent to gather information about the user's skin type, hair type, concerns, known allergies, and price preference.
    Args:
        user_input: The user's input message.
        profile_context: The current user profile context.
    Returns the Intake Agent's response message.
    """
    chat = intake_model.start_chat(enable_automatic_function_calling=True)
    response = chat.send_message(f"User message: {user_input}\nCurrent user profile: {profile_context}")
    return response.text

RECOMMENDATION_AGENT_PROMPT = """You are the Recommendation Agent for a skincare and haircare advisor system.

Responsibilities:
- Recommend skincare and haircare products.
- Create personalized routines.
- Answer ingredient questions.

Guidelines:

- When recommending products, use product_search if product recommendations are needed.
- After selecting products, use update_recommended_products to save them.
- When creating a routine, use update_user_routine after the routine has been finalized.
- When answering ingredient questions, use ingredient_search when ingredient information is required.
- Never invent product names. Use only products returned by the search tool.
- If information is missing, ask only for the minimum follow-up needed.
- If the user requests medical diagnosis, prescription advice, or emergency care, respond:
Requires escalation: <reason>
"""


recommendation_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=RECOMMENDATION_AGENT_PROMPT,
    tools=[product_search, update_recommended_products, update_user_routine, ingredient_search, update_user_profile]
)

def run_recommendation_agent(user_input: str, profile_context : str) -> str:
    """ Run the Recommendation Agent to recommend products and create routines based on the user's profile information.
    Args:
        user_input: The user's input message.
        profile_context: The current user profile context.
    Returns the Recommendation Agent's response message.
    """
    chat = recommendation_model.start_chat(enable_automatic_function_calling=True)
    response = chat.send_message(f"User message: {user_input}\nCurrent user profile: {profile_context}")
    return response.text