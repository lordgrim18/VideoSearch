import re
import os
from django.conf import settings
from decimal import Decimal

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
        print('text:', text)
        subtitles.append({
            'start': Decimal(time_to_seconds(match[1])),
            'text': text
        })

    return subtitles

def save_file_locally(file, video_id):
    local_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    
    file_path = os.path.join(local_dir, f"{video_id}_{file.name}")
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path
