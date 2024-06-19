from django.urls import path

from .subtitle_front_view import SubtitleSearchView, SubtitleListView, SubtitleVideoSearchView

urlpatterns = [
    path("search/", SubtitleSearchView.as_view(), name="subtitle-front-search"),
    path("<str:video_id>/", SubtitleListView.as_view(), name="subtitle-video-list-front"),
    path("<str:video_id>/search/", SubtitleVideoSearchView.as_view(), name="subtitle-video-search-front"),
]