from django.urls import path

from .subtitle_view import SubtitleListAPIView, SubtitleAPIView

urlpatterns = [
    path("search/", SubtitleAPIView.as_view(), name="search_subtitles"), # get - search subtitles
    path("<str:video_id>/", SubtitleListAPIView.as_view(), name="subtitles"), # get - list all subtitles for a video
]