import boto3
from decouple import config
from rest_framework.views import APIView

from api.utils import CustomResponse
from core.dynamo_setup import video_table, subtitle_table
from core.tasks import delete_video_subtitles

from .video_serializer import VideoSerializer


class VideoListAPIView(APIView):
    def get(self, request):
        videos = video_table.scan()['Items']
        serializer = VideoSerializer(data=videos, many=True, context={'request': request})
        if serializer.is_valid():
            return CustomResponse(message="Videos fetched successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error fetching videos", data=serializer.errors).failure_response()  

class VideoAPIView(APIView):

    def get(self, request, video_id):
        video = video_table.get_item(Key={'id': video_id})
        if video.get('Item') is None:
            return CustomResponse(message="Video not found", data={}).failure_response()
        serializer = VideoSerializer(data=video['Item'], context={'request': request})
        if serializer.is_valid():
            return CustomResponse(message="Video fetched successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error fetching video", data=serializer.errors).failure_response()
        
    def post(self, request):
        serializer = VideoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="Video created successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error creating video", data=serializer.errors).failure_response()
    
    def patch(self, request, video_id):
        video = video_table.get_item(Key={'id': video_id})
        if video.get('Item') is None:
            return CustomResponse(message="Video not found", data={}).failure_response()
        serializer = VideoSerializer(video['Item'], data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="Video updated successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error updating video", data=serializer.errors).failure_response()
    
    def delete(self, request, video_id):
        video = video_table.get_item(Key={'id': video_id})
        if video.get('Item') is None:
            return CustomResponse(message="Video not found", data={}).failure_response()
        delete_video_subtitles.delay(video_id)
        return CustomResponse(message="Video deleted successfully", data={}).success_response()
    
class VideoSearchAPIView(APIView):

    def get(self, request):
        keyword = request.query_params.get('keyword')
        if not keyword:
            return CustomResponse(message="No keyword provided", data={}).failure_response()
        print(keyword)
        videos = video_table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('title_lower').contains(keyword.lower())
        )['Items']
        
        serializer = VideoSerializer(data=videos, many=True, context={'request': request})
        if serializer.is_valid():
            data = {
                'count': len(videos),
                'results': serializer.data
            }
            return CustomResponse(message="Videos fetched successfully", data=data).success_response()
        return CustomResponse(message="Error fetching videos", data=serializer.errors).failure_response()
