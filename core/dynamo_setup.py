import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

video_table = dynamodb.Table('Videos')
subtitle_table = dynamodb.Table('Subtitles')

# def create_video(title, video_file_url):
#     video_id = str(uuid.uuid4())
#     video_table.put_item(
#         Item={
#             'id': video_id,
#             'title': title,
#             'video_file_url': video_file_url
#         }
#     )
#     extract_subtitles.delay(video_id)
#     return video_id

# def create_subtitle(video_id, start_time, end_time, text):
#     subtitle_table.put_item(
#         Item={
#             'video_id': video_id,
#             'start_time': start_time,
#             'end_time': end_time,
#             'text': text
#         }
#     )

# def get_video(video_id):
#     response = video_table.get_item(
#         Key={
#             'id': video_id
#         }
#     )
#     return response.get('Item')

# def get_subtitles(video_id):
#     response = subtitle_table.query(
#         KeyConditionExpression=boto3.dynamodb.conditions.Key('video_id').eq(video_id)
#     )
#     return response.get('Items')

# def delete_video(video_id):
#     video_table.delete_item(
#         Key={
#             'id': video_id
#         }
#     )
#     # Also delete associated subtitles
#     subtitles = get_subtitles(video_id)
#     with subtitle_table.batch_writer() as batch:
#         for subtitle in subtitles:
#             batch.delete_item(
#                 Key={
#                     'video_id': subtitle['video_id'],
#                     'start_time': subtitle['start_time']
#                 }
#             )

# def delete_subtitle(video_id, start_time):
#     subtitle_table.delete_item(
#         Key={
#             'video_id': video_id,
#             'start_time': start_time
#         }
#     )


