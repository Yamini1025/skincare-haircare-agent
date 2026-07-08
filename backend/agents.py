import google.generativeai as genai
from tools import get_skin_type_info, get_hair_type_info, update_user_profile

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
    chat = intake_model.start_chat(enable_automatuc_function_calling=True)
    response = chat.send_message(f"User message: {user_input}\nCurrent user profile: {profile_context}")
    return response.text