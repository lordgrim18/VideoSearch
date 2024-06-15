import subprocess
from .models import Video, Subtitle
import re

def time_to_seconds(time_str):
    h, m, s = map(float, time_str.replace(',', '.').split(':'))
    return h * 3600 + m * 60 + s

def parse_srt(srt_content):
    pattern = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n((?:.*(?:\n(?!\d+\n))*)*)")
    matches = pattern.findall(srt_content)

    subtitles = []
    for match in matches:
        subtitles.append({
            'start': time_to_seconds(match[1]),
            'end': time_to_seconds(match[2]),
            'text': match[3]
        })

    return subtitles

def extract_subtitles(video_id):
    video = Video.objects.get(id=video_id)
    video_path = video.video_file.path
    output_path = f"{video_path}.srt"

    subprocess.run(['C:\Program Files (x86)\CCExtractor\ccextractorwin.exe', video_path, '-o', output_path])

    with open(output_path, 'r') as f:
        content = f.read()

    # Process the .srt file and save to Subtitle model
    subtitles = parse_srt(content)
    for subtitle in subtitles:
        Subtitle.objects.create(
            video=video,
            start_time=subtitle['start'],
            end_time=subtitle['end'],
            text=subtitle['text']
        )
