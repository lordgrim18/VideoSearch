import os
from django.conf import settings
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from django.http import HttpRequest, QueryDict

from api.subtitle.subtitle_view import SubtitleSearchAPIView, SubtitleListAPIView, SubtitleVideoSearchAPIView
from api.storage.storage_view import StorageURLAPIView


class SubtitleSearchView(SubtitleSearchAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/subtitle_search.html' 

class SubtitleListView(SubtitleListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/video_subtitle.html'

    def get(self, request, video_id):
        response = super().get(request, video_id)
        data = response.data.get('data')
        video_file_name = data['results']['video_file_name']
        thumbnail_url = os.path.join(settings.MEDIA_ROOT, 'images', f"{video_file_name}.png")
        if os.path.exists(thumbnail_url):
            data['results']['thumbnail_url'] = f"images\{video_file_name}.png"
        return response

class SubtitleVideoSearchView(SubtitleVideoSearchAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/video_subtitle.html'