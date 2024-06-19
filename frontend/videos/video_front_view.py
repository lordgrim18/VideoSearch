from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import redirect

from api.utils import CustomResponse
from api.video.video_view import VideoListAPIView, CreateVideoAPIView
from api.video.video_serializer import VideoSerializer

class VideoListView(VideoListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/video_list.html'

class VideoUploadView(CreateVideoAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/video_upload.html'

    def get(self, request):
        serializer = VideoSerializer()
        return CustomResponse(message="List video fields", data=serializer).success_response()
    
    def post(self, request):
        response = super().post(request)
        if response.status_code == 200:
            return redirect('videos_list_front')
        return response