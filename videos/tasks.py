import subprocess
from celery import shared_task
from decimal import Decimal
import uuid
from .models import Video, Subtitle
from .utils import parse_srt

from .dynamo_setup import video_table, subtitle_table

@shared_task
def extract_subtitles(video_id):
    print('Task started, video_id:', video_id)
    # video = Video.objects.get(id=video_id)
    video = video_table.get_item(Key={'id': video_id})
    video = video['Item']

    video_path = video['video_file_url']
    output_path = f"{video_path}.srt"

    subprocess.run(['C:\Program Files (x86)\CCExtractor\ccextractorwin.exe', video_path, '-o', output_path])

    with open(output_path, 'r') as f:
        content = f.read()

    # Process the .srt file and save to Subtitle model
    subtitles = parse_srt(content)
    with subtitle_table.batch_writer(overwrite_by_pkeys=['video_id', 'start_time']) as batch:
        for subtitle in subtitles:
            batch.put_item(
                Item={
                    'video_id': video_id,
                    'start_time': Decimal(subtitle['start']),
                    'text': subtitle['text'],
                    'text_lower': subtitle['text'].lower()
                }
            )   