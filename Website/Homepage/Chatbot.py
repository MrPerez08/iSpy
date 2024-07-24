import io
from google.cloud import videointelligence
import PIL.Image
import google.generativeai as genai
import os
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from google.generativeai.types import HarmCategory, HarmBlockThreshold
os.environ["GEMINI_API_KEY"] = "AIzaSyCHh3PMRXTlWtc_9YmmytbdN4KMpxqtt4M"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

img=PIL.Image.open('IMG_0280.jpg') #<- IMPORT IMAGE

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
    system_instruction="explain the image",                         
)
response= model.generate_content(img)
print(response.text)

#cant tweak response (sounde like chatgpt)

# Your Google Cloud Video Intelligence API key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/key.json"

# Replace with your video file path
video_path = "path/to/your/video.mp4"

# Create a video intelligence client
client = videointelligence.VideoIntelligenceServiceClient()

# Load the video file
with io.open(video_path, 'rb') as video_file:
    content = video_file.read()

# Create a video object
video = videointelligence.Video(content=content)

# Analyze labels
response = client.annotate_video(
    input_content=video,
    features=[videointelligence.Feature.LABEL_DETECTION],
)

# Access the labels
labels = response.annotation_results[0].segment_label_annotations

# Process the labels and send to LLM (Gemini in the future)
for label in labels:
    # ... extract data and format for Gemini's input ...
    # Send to Gemini:  llm_response = YOUR_LLM_API.process_video(data) 