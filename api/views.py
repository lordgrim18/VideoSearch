import uuid
from rest_framework.views import APIView

from api.utils import CustomResponse
from core.dynamo_setup import video_table, subtitle_table
from core.utils import save_file_locally

from .serializer import VideoSerializer


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
    