from django.urls import path

from .subtitle_front_view import SubtitleSearchView

urlpatterns = [
    path("search/", SubtitleSearchView.as_view(), name="subtitle-front-search"),
]