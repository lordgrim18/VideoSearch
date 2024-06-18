import os
import uuid
import boto3
from decouple import config
from django.conf import settings
from rest_framework import serializers

from core.dynamo_setup import video_table, subtitle_table
from core.utils import save_file_locally
from core.tasks import extract_subtitles

from api.utils import CustomResponse

class VideoSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    title = serializers.CharField()
    video_file_name = serializers.CharField(required=False)

    def validate_title(self, value):
        if video_table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('title').eq(value))['Items']:
            raise serializers.ValidationError('Video with this title already exists')
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        title = request.data['title']
        video_file = request.FILES['video_file']
        video_id = str(uuid.uuid4())
        video_file_name = f"{video_id}_{video_file.name}"
        local_file_url = save_file_locally(video_file, video_file_name)
        try:
            video_table.put_item(
                Item={
                    'id': video_id,
                    'title': title,
                    'video_file_name': video_file_name
                }
            )
        except Exception as e:
            print('Error:', e)
            raise serializers.ValidationError('Error creating video')
        finally:
            extract_subtitles.delay(video_id, local_file_url, video_file_name)

        video = video_table.get_item(Key={'id': video_id})['Item']
        return video
    
    def update(self, instance, validated_data):
        video_id = instance['id']
        video_table.update_item(
            Key={'id': video_id},
            UpdateExpression='SET title = :title',
            ExpressionAttributeValues={':title': validated_data['title']}
        )
        video = video_table.get_item(Key={'id': video_id})['Item']
        return video
    
class SubtitleSerializer(serializers.Serializer):
    start_time = serializers.DecimalField(max_digits=10, decimal_places=3)
    text = serializers.CharField()

class VideoSubtitleSerializer(serializers.Serializer):
    video_id = serializers.CharField()
    video_title = serializers.CharField()
    subtitles = SubtitleSerializer(many=True)

class StorageSerializer(serializers.Serializer):
    object_name = serializers.CharField(required=True)

    def validate(self, data):
        object_name = data.get('object_name')
        s3 = boto3.client('s3')
        bucket_name = config('BUCKET_NAME')
        bucket_objs = s3.list_objects_v2(Bucket=bucket_name)

        if bucket_objs.get('Contents') is None:
            raise serializers.ValidationError('No Objects found inside storage')
        if object_name not in [file['Key'] for file in bucket_objs['Contents']]:
            raise serializers.ValidationError('Object not found in storage')
        return data

    def retrieve(self, object_name):
        s3 = boto3.client('s3')
        bucket_name = config('BUCKET_NAME')

        download_path = os.path.join(settings.MEDIA_ROOT, 'videos', object_name)
        if os.path.exists(download_path):
            return CustomResponse(message="File already exists", data={'download_path': download_path}).failure_reponse()
        
        s3.download_file(bucket_name, object_name, download_path)
        return CustomResponse(message="File downloaded successfully", data={'download_path': download_path}).success_response()
    
    def destroy(self, object_name):
        s3 = boto3.client('s3')
        bucket_name = config('BUCKET_NAME')
        s3.delete_object(Bucket=bucket_name, Key=object_name)

class StorageURLSerializer(StorageSerializer):
    expires_in = serializers.IntegerField(required=False)
    presigned_url = serializers.SerializerMethodField()

    def validate(self, data):
        super().validate(data)
        expires_in = data.get('expires_in', 3600)
        data['expires_in'] = expires_in
        return data
    
    def get_presigned_url(self, validated_data):
        print(validated_data)
        object_name = validated_data['object_name']
        expires_in = validated_data['expires_in']
        print(object_name, expires_in)
        s3 = boto3.client('s3')
        bucket_name = config('BUCKET_NAME')
        print(bucket_name)
        url = s3.generate_presigned_url(
            'get_object', 
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expires_in
        )
        print(url)
        return url