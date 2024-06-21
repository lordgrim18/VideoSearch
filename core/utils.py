import re
import os
import os
import cv2
from django.conf import settings

def time_to_seconds(time_str):
    h, m, s = map(float, time_str.split(',')[0].split(':'))
    return h * 3600 + m * 60 + s

def parse_srt(srt_content):
    pattern = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n((?:.*(?:\n(?!\d+\n))*)*)")
    matches = pattern.findall(srt_content)

    subtitles = []
    for match in matches:
        text = re.sub(r'\s+', ' ', match[3].strip())  # Clean up spaces and newlines
        text = re.sub(r'[^a-zA-Z0-9\s.,?!&\'"@#\-]', '', text)  # Remove unwanted characters, keep alphabets, numbers, spaces, and specific symbols
        subtitles.append({
            'start': time_to_seconds(match[1]),
            'text': text
        })

    return subtitles

def save_file_locally(file, video_file_name):
    local_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    
    file_path = os.path.join(local_dir, video_file_name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path

def create_thumbnail(file_path, video_file_name):
    """Extract the first frame from video"""
    cap = cv2.VideoCapture(file_path)
    for i in range(28):
        cap.read()
    success, image = cap.read()
    if success:
        local_dir = os.path.join(settings.MEDIA_ROOT, 'images')
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        image_path = os.path.join(local_dir, f"{video_file_name}.png")
        cv2.imwrite(image_path, image)
