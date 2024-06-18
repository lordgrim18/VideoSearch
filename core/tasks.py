import os
import boto3
import subprocess
from decimal import Decimal
from decouple import config
from celery import shared_task

from .utils import parse_srt
from .dynamo_setup import subtitle_table, video_table

@shared_task
def extract_subtitles(video_id, local_file_url, video_file_name):
    output_path = f"{local_file_url}.srt"

    subprocess.run(['C:\Program Files (x86)\CCExtractor\ccextractorwin.exe', local_file_url, '-o', output_path])

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

    # s3 = boto3.client('s3')
    # bucket_name = config('BUCKET_NAME')
    # print(f"Uploading {local_file_url} to S3")
    # s3.upload_file(local_file_url, bucket_name, video_file_name)

    os.remove(local_file_url)
    os.remove(output_path)

@shared_task
def delete_video_subtitles(video_id):
    # Also delete associated subtitles
    video_table.delete_item(Key={'id': video_id})
    subtitles = subtitle_table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('video_id').eq(video_id))
    with subtitle_table.batch_writer() as batch:
        for subtitle in subtitles['Items']:
            batch.delete_item(
                Key={
                    'video_id': subtitle['video_id'],
                    'start_time': subtitle['start_time']
                }
            )