from django.urls import path

from .views import VideoListAPIView, VideoAPIView

urlpatterns = [
    path("videos/", VideoListAPIView.as_view(), name="videos"), # get - list all videos

    path("videos/create/", VideoAPIView.as_view(), name="create_video"), # post - create a video
    path("videos/<str:video_id>/", VideoAPIView.as_view(), name="video"), # get - a single video
    path("videos/update/<str:video_id>/", VideoAPIView.as_view(), name="update_video"), # patch - update a video
    
]