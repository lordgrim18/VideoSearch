from rest_framework.renderers import TemplateHTMLRenderer

from api.utils import CustomResponse
from api.subtitle.subtitle_view import SubtitleSearchAPIView


class SubtitleSearchView(SubtitleSearchAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'frontend/subtitle_search.html' 