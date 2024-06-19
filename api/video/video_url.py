from django.urls import path

from .video_view import VideoListAPIView, CreateVideoAPIView, SingleVideoAPIView, VideoSearchAPIView

urlpatterns = [
    path("", VideoListAPIView.as_view(), name="list_videos"), # get - list all videos
    path("create/", CreateVideoAPIView.as_view(), name="create_video"), # post - create a video
    path("search/", VideoSearchAPIView.as_view(), name="search_videos"), # get - search videos
    
    path("<str:video_id>/", SingleVideoAPIView.as_view(), name="video"), # get - a single video
    path("update/<str:video_id>/", SingleVideoAPIView.as_view(), name="update_video"), # patch - update a video
    path("delete/<str:video_id>/", SingleVideoAPIView.as_view(), name="delete_video"), # delete - delete a video
]