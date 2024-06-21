import boto3
from rest_framework.views import APIView

from api.utils import CustomResponse
from core.dynamo_setup import video_table, subtitle_table
from core.tasks import delete_video_subtitles, delete_video_from_s3

from .video_serializer import VideoSerializer


class VideoListAPIView(APIView):
    def get(self, request):
        videos = video_table.scan()['Items']
        serializer = VideoSerializer(data=videos, many=True, context={'request': request})
        if serializer.is_valid():
            data = {
                'count': len(videos),
                'results': serializer.data
            }
            return CustomResponse(message="Videos fetched successfully", data=data).success_response()
        return CustomResponse(message="Error fetching videos", data=serializer.errors).failure_response()  

class CreateVideoAPIView(APIView):

    def post(self, request):
        try:
            video_file = request.FILES['video_file']
        except:
            return CustomResponse(message="Video file not found", data={}).failure_response()
        if not video_file.name.endswith('.mp4'):
            return CustomResponse(message="Video file must be in mp4 format", data={}).failure_response()
        
        serializer = VideoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="Video created successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error creating video", data=serializer.errors).failure_response()
    
class SingleVideoAPIView(APIView):

        def get(self, request, video_id):
            video = video_table.get_item(Key={'id': video_id})
            if video.get('Item') is None:
                return CustomResponse(message="Video not found", data={}).failure_response()
            serializer = VideoSerializer(data=video['Item'], context={'request': request})
            if serializer.is_valid():
                return CustomResponse(message="Video fetched successfully", data=serializer.data).success_response()
            return CustomResponse(message="Error fetching video", data=serializer.errors).failure_response()
        
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
            video_name = video['Item']['video_file_name']
            delete_video_subtitles.delay(video_id)
            delete_video_from_s3.delay(video_name)
            return CustomResponse(message="Video deleted successfully", data={}).success_response()

class VideoSearchAPIView(APIView):

    def get(self, request):
        keyword = request.query_params.get('keyword', '')
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
