from rest_framework.renderers import TemplateHTMLRenderer

from api.subtitle.subtitle_view import SubtitleSearchAPIView, SubtitleListAPIView, SubtitleVideoSearchAPIView


class SubtitleSearchView(SubtitleSearchAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/subtitle_search.html' 

class SubtitleListView(SubtitleListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/video_subtitle.html'

class SubtitleVideoSearchView(SubtitleVideoSearchAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/video_subtitle.html'