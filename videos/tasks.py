import subprocess
from celery import shared_task
import time

from videos.models import Video, Subtitle
from videos.utils import parse_srt

@shared_task
def extract_subtitles(video_id):
    print('Task started, video_id:', video_id)
    video = Video.objects.get(id=video_id)
    video_path = video.video_file.path
    output_path = f"{video_path}.srt"

    subprocess.run(['ccextractor', video_path, '-o', output_path])

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