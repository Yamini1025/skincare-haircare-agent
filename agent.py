import os
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT
from tools import get_skin_type_info

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT,
    tools=[get_skin_type_info]
)

def run_agent():
    print("Skincare/Haircare Advisor")
    print("Type 'quit' to exit\n")

    chat = model.start_chat(enable_automatic_function_calling=True)

    while True:
        user_input = input("Enter: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            break
        if not user_input:
            continue

        response = chat.send_message(user_input)
        print(f"\nSkincare/Haircare Advisor: {response.text}")

if __name__ == "__main__":
    run_agent()