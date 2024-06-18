from django.urls import path

from .views import VideoListAPIView, VideoAPIView, SubtitleAPIView, StorageListAPIView, StorageAPIView, StorageURLAPIView

urlpatterns = [
    path("videos/", VideoListAPIView.as_view(), name="list_videos"), # get - list all videos
    path("videos/create/", VideoAPIView.as_view(), name="create_video"), # post - create a video
    path("videos/<str:video_id>/", VideoAPIView.as_view(), name="video"), # get - a single video
    path("videos/update/<str:video_id>/", VideoAPIView.as_view(), name="update_video"), # patch - update a video
    path("videos/delete/<str:video_id>/", VideoAPIView.as_view(), name="delete_video"), # delete - delete a video

    path("subtitles/<str:video_id>/", SubtitleAPIView.as_view(), name="subtitles"), # get - list all subtitles for a video

    path("storage/url/", StorageURLAPIView.as_view(), name="storage_url"), # get - generate a presigned url for a file in bucket

    path("storage/", StorageListAPIView.as_view(), name="storage"), # get - list all files in bucket 
    path("storage/delete/<str:object_name>/", StorageAPIView.as_view(), name="delete_file"), # delete - delete a file from bucket 
    path("storage/<str:object_name>/", StorageAPIView.as_view(), name="file"), # get - download a file from bucket

]