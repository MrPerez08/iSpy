# file_switch.py

from video_analyzer import analyze_video
from img_analyzer import analyze_image
from chatbot import analyze_text

# Dictionary mapping
analyzers = {
    'video': analyze_video,
    'image': analyze_image,
    'text': analyze_text,
}

def analyze_file(file_type, file):
    # Get the analyzer function from analyzers dictionary
    analyzer_function = analyzers.get(file_type, lambda f: "Unknown file type")
    return analyzer_function(file)
