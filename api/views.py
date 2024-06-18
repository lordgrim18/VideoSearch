import os
import boto3
from decouple import config
from rest_framework.views import APIView
from django.conf import settings

from api.utils import CustomResponse
from core.dynamo_setup import video_table, subtitle_table
from core.tasks import delete_video_subtitles

from .serializer import VideoSerializer, VideoSubtitleSerializer, StorageSerializer


class VideoListAPIView(APIView):
    def get(self, request):
        videos = video_table.scan()['Items']
        serializer = VideoSerializer(data=videos, many=True)
        if serializer.is_valid():
            return CustomResponse(message="Videos fetched successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error fetching videos", data=serializer.errors).failure_reponse()  

class VideoAPIView(APIView):

    def get(self, request, video_id):
        video = video_table.get_item(Key={'id': video_id})
        if video.get('Item') is None:
            return CustomResponse(message="Video not found", data={}).failure_reponse()
        serializer = VideoSerializer(data=video['Item'])
        if serializer.is_valid():
            return CustomResponse(message="Video fetched successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error fetching video", data=serializer.errors).failure_reponse()
        
    def post(self, request):
        serializer = VideoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="Video created successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error creating video", data=serializer.errors).failure_reponse()
    
    def patch(self, request, video_id):
        video = video_table.get_item(Key={'id': video_id})
        if video.get('Item') is None:
            return CustomResponse(message="Video not found", data={}).failure_reponse()
        serializer = VideoSerializer(video['Item'], data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="Video updated successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error updating video", data=serializer.errors).failure_reponse()
    
    def delete(self, request, video_id):
        video = video_table.get_item(Key={'id': video_id})
        if video.get('Item') is None:
            return CustomResponse(message="Video not found", data={}).failure_reponse()
        delete_video_subtitles.delay(video_id)
        return CustomResponse(message="Video deleted successfully", data={}).success_response()
    
class SubtitleAPIView(APIView):
    def get(self, request, video_id):
        subtitles = subtitle_table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('video_id').eq(video_id))
        if subtitles.get('Items') is None:
            return CustomResponse(message="No subtitles found", data={}).failure_reponse()
        
        video_title = video_table.get_item(Key={'id': video_id})['Item']['title']
        
        subtitles = [{
            'start_time': str(subtitle['start_time']),
            'text': subtitle['text']
        } for subtitle in subtitles['Items']]
        data = {
            'video_id': video_id,
            'video_title': video_title,
            'subtitles': subtitles
        }

        serializer = VideoSubtitleSerializer(data=data)
        if serializer.is_valid():
            return CustomResponse(message="Subtitles fetched successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error fetching subtitles", data=serializer.errors).failure_reponse()
    
class StorageListAPIView(APIView):

    def get(self, request):
        s3 = boto3.client('s3')
        bucket_name = config('BUCKET_NAME')
        bucket_objs = s3.list_objects_v2(Bucket=bucket_name)
        if bucket_objs.get('Contents') is None:
            return CustomResponse(message="No Objects found inside storage", data={}).failure_reponse()
        
        files = [{'object_name': file['Key']} for file in bucket_objs['Contents']]
        serializer = StorageSerializer(data=files, many=True)
        if serializer.is_valid():
            return CustomResponse(message="Storage objects fetched successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error fetching storage objects", data=serializer.errors).failure_reponse()

class StorageAPIView(APIView):

    def get(self, request, object_name):
        serializer = StorageSerializer(data={'object_name': object_name})
        if serializer.is_valid():
            download = serializer.retrieve(object_name)
            return download
        return CustomResponse(message="Error fetching object", data=serializer.errors).failure_response()

    def delete(self, request, object_name):
        serializer = StorageSerializer(data={'object_name': object_name})
        if serializer.is_valid():
            serializer.destroy(object_name)
            return CustomResponse(message="Object deleted successfully", data={}).success_response()
        return CustomResponse(message="Error deleting object", data=serializer.errors).failure_reponse()