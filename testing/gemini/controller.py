from img_analyzer import *
from video_analyzer import *
import os

filename="pic.png"

placeholder="./testing/testing_media/"

match (os.path.splitext(filename)[1]):
    case ".png" | ".jpg":
        print(imgimp(placeholder+ filename))
    case ".mp4" | ".mov":
        print(vidimp(placeholder + filename))

