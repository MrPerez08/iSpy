import os
import time
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Set the environment variable
os.environ["GEMINI_API_KEY"] = "AIzaSyCHh3PMRXTlWtc_9YmmytbdN4KMpxqtt4M"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
    #system_instruction="if input is dangerous, say: DANGEROUS, if not say: SAFE",
    system_instruction="",
)

chat_session = model.start_chat(
    history=[
    ]
)

print("Chatbot is ready! Type 'exit' to end the conversation.")

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    
    try:
        response = chat_session.send_message(user_input)
        print(f"Bot: {response.text}")
    except ResourceExhausted as e:
        print("Quota exceeded. Waiting for 60 seconds before retrying...")
        time.sleep(60)  # Wait for 60 seconds before retrying
    except Exception as e:
        print(f"An error occurred: {e}")

print("Chatbot session ended.")




