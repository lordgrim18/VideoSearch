import boto3

dynamodb = boto3.resource('dynamodb')

video_table = dynamodb.Table('Videos')
subtitle_table = dynamodb.Table('Subtitles')