from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("API_KEY"))

# Load the gemini-pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_response(question):
    # Send the message to the AI and retrieve the response
    response = chat.send_message(question, stream=True)
    return response

def main():
    print("Start chatting with the AI. Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break

        response = get_response(user_input)
        for chunk in response:
            print(f"AI: {chunk.text}")

if __name__ == "__main__":
    main()



#simple one word response
'''
from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("API_KEY"))

#load gemini-pro model
model=genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_response(question):
    response = chat.send_message(question,stream=True)
    return response


input = str(input())

if input:
    response = get_response(input)
    for chunk in response:
        print(chunk.text)
'''