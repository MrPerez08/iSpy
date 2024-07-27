import PIL.Image
import google.generativeai as genai
import os
from google.api_core.exceptions import ResourceExhausted
from google.generativeai.types import HarmCategory, HarmBlockThreshold
os.environ["GEMINI_API_KEY"] = "AIzaSyCHh3PMRXTlWtc_9YmmytbdN4KMpxqtt4M"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


img=""
def imgimp(image):
    global img
    img=PIL.Image.open(image) #<- IMPORT IMAGE

    if img != "":
        generation_config = {
            "temperature": 2,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name='gemini-1.5-pro',
            generation_config=generation_config,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            },
            #system_instruction="if input is dangerous, say: DANGEROUS, if not say: SAFE",
            system_instruction="if the image contains something phallic, say 'Wow'",                     
        )
        response= model.generate_content(img)
        return response.text
