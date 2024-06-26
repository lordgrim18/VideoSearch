import uuid
import boto3
from rest_framework import serializers

from core.dynamo_setup import video_table
from core.utils import save_file_locally, create_thumbnail
from core.tasks import extract_subtitles, save_to_s3

class VideoSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    title = serializers.CharField()
    video_file_name = serializers.CharField(required=False)

    def validate_title(self, value):
        request = self.context.get('request')
        if request.method == 'GET':
            return value
        if video_table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('title').eq(value))['Items']:
            raise serializers.ValidationError('Video with this title already exists')
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        title = validated_data['title']
        video_file = request.FILES['video_file']
        video_id = str(uuid.uuid4())
        video_file_name = f"{video_id}_{video_file.name}"
        local_file_url = save_file_locally(video_file, video_file_name)
        create_thumbnail(local_file_url, video_file_name)
        video_table.put_item(
            Item={
                'id': video_id,
                'title': title,
                'title_lower': title.lower(),
                'video_file_name': video_file_name
            }
        )
        extract_subtitles.delay(video_id, local_file_url, video_file_name)
        save_to_s3.delay(local_file_url, video_file_name, local_file_url)

        video = video_table.get_item(Key={'id': video_id})['Item']
        return video
    
    def update(self, instance, validated_data):
        video_id = instance['id']
        video_table.update_item(
            Key={'id': video_id},
            UpdateExpression='SET title = :title, title_lower = :title_lower',
            ExpressionAttributeValues={':title': validated_data['title'], ':title_lower': validated_data['title'].lower()}
        )
        video = video_table.get_item(Key={'id': video_id})['Item']
        return video
    