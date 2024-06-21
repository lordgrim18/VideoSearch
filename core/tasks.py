import os
import boto3
import subprocess
from decimal import Decimal
from decouple import config
from celery import shared_task
from django.conf import settings

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

@shared_task
def save_to_s3(file_path, file_name, local_file_url):
    s3 = boto3.client('s3')
    bucket_name = config('BUCKET_NAME')
    print(f"Uploading {file_path} to S3")
    s3.upload_file(file_path, bucket_name, file_name)

    os.remove(local_file_url)
    os.remove(f"{local_file_url}.srt")

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

@shared_task
def delete_video_from_s3(video_name):
    s3 = boto3.client('s3')
    bucket_name = config('BUCKET_NAME')
    s3.delete_object(Bucket=bucket_name, Key=video_name)

@shared_task
def delete_video_thumbnail(video_name):
    image_path = os.path.join(settings.MEDIA_ROOT, 'images', f"{video_name}.png")
    if os.path.exists(image_path):
        os.remove(image_path)