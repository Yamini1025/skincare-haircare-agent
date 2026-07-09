import google.generativeai as genai
from tools import get_skin_type_info, get_hair_type_info, update_user_profile, product_search, update_recommended_products, ingredient_search, product_search_with_safety_check

INTAKE_AGENT_PROMPT = """
You are the Intake Agent for a skincare and haircare advisor system. Your only task is to gather information about the user's skin type, hair type, 
concerns, known allergies, and price preference. You will ask the user questions to collect this information.
Rules - 
- Always ask about skin type (dry/oily/combination/sensitive/normal) or hair type (straight, wavy, curly, coily) if unknown.
- Only ask questions to gather information about the user's skin type, hair type, concerns, known allergies, and price preference. Do not provide any recommendations or advice.
- If the user provides information about their skin type, hair type, concerns, known allergies, or price preference, update the user profile accordingly.
- Do not provide any recommendations or advice. Your only task is to gather information and update the user profile.
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

RESEARCH_AGENT_PROMPT = """
You are the Research Agent for a skincare and haircare advisor system. Your only task is to find relevant products based on the user's skin type, 
hair type, concerns, known allergies, and price preference.
Rules -
- Only recommend products/routines when user explicitly uses phrases such as "recommend", "suggest", "what should I do", or "what should I use"
- Always call product_search before recommending any product
- After calling product_search and selecting products to recommend, always call update_recommended_products with the product names
- If the user asks for a medical diagnosis, prescription, or explicitly asks for a human, respond with: Requires escalation: [reason]
- Add a one sentence disclaimer when recommending active ingredients like retinol or acids and when recommending categories like hair growth treatments/medication, anti-dandruff actives, strong exfoliants, or chemical processing products
- If a response has multiple disclaimers, order them as such : first give the "I am not a doctor" disclaimer, then give the active ingredients disclaimer, then give the product/brand disclaimer
- Categories for products include: cleanser, moisturizer, sunscreen, serum, spot treatment, BHA treatment, AHA treatment, exfoliant, shampoo, conditioner, hair serum, curl cream, deep conditioner, hair mask
- Give information about the products you recommend, including their ingredients, usage instructions, and why they are suitable for the user.
- Do NOT build routines, that is the Planner Agent's job
"""
research_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=RESEARCH_AGENT_PROMPT,
    tools=[product_search_with_safety_check, ingredient_search, update_recommended_products]
)

def run_research_agent(user_input: str, profile_context : str) -> str:
    """ Run the Research Agent to find relevant products based on the user's skin type, hair type, concerns, known allergies, and price preference.
    Args:
        user_input: The user's input message.
        profile_context: The current user profile context.
    Returns the Research Agent's response message.
    """
    chat = research_model.start_chat(enable_automatic_function_calling=True)
    response = chat.send_message(f"User profile: {profile_context}\nFind products for: {user_input}")
    return response.text

SAFETY_AGENT_PROMPT = """
You are the Safety Agent for a skincare and haircare advisor system. Your only task is to check if ingredients of a product are suitable for the user.
Check products for ingredient conflicts with the user's allergies. Flag any product that contains an ingredient the user is allergic to.
"""

safety_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SAFETY_AGENT_PROMPT,
    tools=[ingredient_search]
)

def run_safety_agent(products: list, allergies : list) -> list:
    """ Run the Safety Agent to check if ingredients of a product are suitable for the user.
    Args:
        products: A list of products to check.
        allergies: A list of the user's known allergies.
    Returns the Safety Agent's response message.
    """
    chat = safety_model.start_chat(enable_automatic_function_calling=True)
    response = chat.send_message(f"User allergies: {allergies}\nCheck products for safety: {products}")
    return response.text