import os
import time
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from google.generativeai.types import HarmCategory, HarmBlockThreshold

video_file_name=""
def vidimp(video):
    global video_file_name
    video_file_name=video #<- IMPORT IMAGE

    if video_file_name != "":
        os.environ["GEMINI_API_KEY"] = "AIzaSyCHh3PMRXTlWtc_9YmmytbdN4KMpxqtt4M"
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        print(f"Uploading file...")
        video_file = genai.upload_file(path=video_file_name)
        print(f"Completed upload: {video_file.uri}")


        while video_file.state.name == "PROCESSING":
            print('.', end='')
            time.sleep(10)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError(video_file.state.name)

        file = genai.get_file(name=video_file.name)
        print(f"Retrieved file '{file.display_name}' as: {video_file.uri}")

        # Create the prompt.

        # The Gemini 1.5 models are versatile and work with multimodal prompts
        model = genai.GenerativeModel(model_name="gemini-1.5-pro",
            generation_config = {
                "temperature": 2,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            },
            system_instruction="What are the viewers talking about?"
        )

        # Make the LLM request.
        print("Making LLM inference request...")
        response = model.generate_content([video_file],request_options={"timeout": 600})
        return response.text

