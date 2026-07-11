import google.generativeai as genai
from tools import get_skin_type_info, get_hair_type_info, update_user_profile, product_search, update_recommended_products, ingredient_search, product_search_with_safety_check, update_user_routine
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

RESEARCH_AGENT_PROMPT = """
You are the Research Agent for a skincare and haircare advisor system. Your only task is to find relevant products based on the user's skin type,
hair type, concerns, known allergies, and price preference.
Rules -
- Only recommend products/routines when user explicitly uses phrases such as "recommend", "suggest", "what should I do", or "what should I use" OR when another agent requests product research.
- Always call product_search_with_safety_check before recommending any product.
- Use the product search results as the source of truth. Prefer actual products from the product database and include their exact names.
- Do not invent products, do not use placeholders, and do not output generic step names when real products are available.
- After calling product_search_with_safety_check and selecting products to recommend, always call update_recommended_products with the product names.
- If the user asks for a medical diagnosis, prescription, or explicitly asks for a human, respond with: Requires escalation: [reason]
- Add a one sentence disclaimer when recommending active ingredients like retinol or acids and when recommending categories like hair growth treatments/medication, anti-dandruff actives, strong exfoliants, or chemical processing products.
- If a response has multiple disclaimers, order them as such: first give the "I am not a doctor" disclaimer, then the active ingredients disclaimer, then the product/brand disclaimer.
- Categories for products include: cleanser, moisturizer, sunscreen, serum, spot treatment, BHA treatment, AHA treatment, exfoliant, shampoo, conditioner, hair serum, curl cream, deep conditioner, hair mask.
- Give information about the products you recommend, including their ingredients, usage instructions, and why they are suitable for the user.
- If the user provides new information about their skin type, hair type, concerns, allergies, or price preference, call update_user_profile before recommending products.
- Do NOT build routines; that is the Planner Agent's job.
"""
research_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=RESEARCH_AGENT_PROMPT,
    tools=[product_search_with_safety_check, ingredient_search, update_recommended_products, update_user_profile]
)

def run_research_agent(user_input: str, profile_context : str) -> str:
    """ Run the Research Agent to find relevant products based on the user's skin type, hair type, concerns, known allergies, and price preference.
    Args:
        user_input: The user's input message.
        profile_context: The current user profile context.
    Returns the Research Agent's response message.
    """
    chat = research_model.start_chat(enable_automatic_function_calling=True)
    response = chat.send_message(f"User profile: {profile_context}\nUser request: {user_input}")
    return response.text

PLANNER_AGENT_PROMPT = """
You are the Planner Agent for a skincare and haircare advisor system. Your only task is to build a skincare or haircare routine for the user.
Rules:
- The research step has already selected the products. Do not perform additional product selection.
- Every routine step that requires a product MUST use one of the products provided by the research step.
- If no suitable product was provided for a step, omit that step instead of inventing one.
- Do not invent products, do not use generic placeholders, and do not replace real product names with vague labels like "cleanser" or "serum" when a specific product was found.
- For skincare routines, order the steps as: cleanser -> toner/treatment -> serum -> moisturizer -> sunscreen (for AM) and cleanser -> toner/treatment -> serum -> moisturizer (for PM).
- If the user asks for a morning routine only, create only AM steps and leave PM empty. If the user asks for an evening routine only, create only PM steps. If no time of day is specified, create both AM and PM.
- For haircare routines, order the steps as deemed fit for the user's specific hair type and concerns.
- After creating the routine, always call update_user_routine to save the morning/evening routine.
- Do not only describe the routine in text.
"""

planner_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=PLANNER_AGENT_PROMPT,
    tools=[update_user_routine]
)

def run_planner_agent(user_input: str, profile_context : str) -> str:
    """ Run the Planner Agent to build a skincare or haircare routine for the user.
    Args:
        user_input: The user's input message.
        profile_context: The current user profile context.
    Returns the Planner Agent's response message.
    """
    run_research_agent(f"recommend products for: {user_input}", profile_context)

    products = state.user_recommended_products
    
    chat = planner_model.start_chat(enable_automatic_function_calling=True)
    response = chat.send_message(f"User profile: {profile_context}\nRecommended products: {products} Build a routine using ONLY these products.")
    return response.text