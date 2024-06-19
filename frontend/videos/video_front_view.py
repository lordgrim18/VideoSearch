from rest_framework.renderers import TemplateHTMLRenderer

from api.video.video_view import VideoListAPIView

class VideoListView(VideoListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/video_list.html'