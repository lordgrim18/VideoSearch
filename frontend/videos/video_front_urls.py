from django.urls import path

from .video_front_view import VideoListView, VideoUploadView, VideoSearchView, SingleVideoView


urlpatterns = [
    path("", VideoListView.as_view(), name="videos_list_front"),
    path("upload/", VideoUploadView.as_view(), name="upload"),
    path("search/", VideoSearchView.as_view(), name="video-search-front"),
    path("update/<str:video_id>/", SingleVideoView.as_view(), name="update-video-front"),
    path("delete/<str:video_id>/", SingleVideoView.as_view(), name="delete-video-front"),

]