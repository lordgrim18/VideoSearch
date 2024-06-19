from django.urls import path, include
from .view import SearchAPIView

urlpatterns = [
    path("videos/", include("api.video.video_url")), # video urls
    path("subtitles/", include("api.subtitle.subtitle_url")), # subtitle urls
    path("storage/", include("api.storage.storage_url")), # storage urls

    path("search/", SearchAPIView.as_view(), name="search"), # get - search videos and subtitles

]