from django.urls import path

from .subtitle_view import SubtitleListAPIView, SubtitleSearchAPIView, SubtitleVideoSearchAPIView

urlpatterns = [
    path("search/", SubtitleSearchAPIView.as_view(), name="search_subtitles"), # get - search subtitles
    path("<str:video_id>/", SubtitleListAPIView.as_view(), name="subtitles"), # get - list all subtitles for a video
    path("<str:video_id>/search/", SubtitleVideoSearchAPIView.as_view(), name="search_video_subtitles"), # get - search subtitles for a video
]