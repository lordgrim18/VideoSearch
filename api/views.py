from rest_framework.views import APIView

from api.utils import CustomResponse
from core.dynamo_setup import video_table, subtitle_table

from .serializer import VideoSerializer


class VideoListAPIView(APIView):
    def get(self, request):
        videos = video_table.scan()['Items']
        serializer = VideoSerializer(data=videos, many=True)
        if serializer.is_valid():
            return CustomResponse(message="Videos fetched successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error fetching videos").failure_reponse()   
        