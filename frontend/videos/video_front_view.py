from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import redirect

from api.utils import CustomResponse
from api.video.video_view import VideoListAPIView, CreateVideoAPIView, VideoSearchAPIView, SingleVideoAPIView
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
    
class VideoSearchView(VideoSearchAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/video_list.html'

class SingleVideoView(SingleVideoAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/video_update.html'

    def get(self, request, video_id):
        response = super().get(request, video_id)
        extra_param = request.GET.get('extra_param')
        data = response.data
        return Response({'extra_param': extra_param, 'data': data})
    
    def post(self, request, video_id):
        request_method = request.POST.get('_method')
        print(request_method)
        if request_method == 'DELETE':
            print('delete')
            response = super().delete(request, video_id)
            print(response)
            print(response.data)
            if response.status_code == 200:
                return redirect('videos_list_front')
            return response
        else:
            response = super().patch(request, video_id)
            if response.status_code == 200:
                return redirect('videos_list_front')
            return response