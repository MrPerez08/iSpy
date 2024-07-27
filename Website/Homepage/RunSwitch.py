# main.py

from file_switch import analyze_file

# Test files
video_file = "example_video.mp4"
image_file = "example_image.png"
text_file = "example_text.txt"

# Analyze the files
video_result = analyze_file('video', video_file)
image_result = analyze_file('image', image_file)
text_result = analyze_file('text', text_file)
unknown_result = analyze_file('audio', "example_audio.mp3")  # Test with an unknown file type

# Print results
print(video_result)   # Output: Analyzing video file: example_video.mp4
print(image_result)   # Output: Analyzing image file: example_image.png
print(text_result)    # Output: Analyzing text file: example_text.txt
print(unknown_result) # Output: Unknown file type
