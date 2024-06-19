from django.urls import path

from .video_front_view import VideoListView, VideoUploadView


urlpatterns = [
    path("", VideoListView.as_view(), name="videos_list_front"),
    path("upload/", VideoUploadView.as_view(), name="upload"),

]