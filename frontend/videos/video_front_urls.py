from django.urls import path

from .video_front_view import VideoListView


urlpatterns = [
    path("", VideoListView.as_view(), name="home"),
]