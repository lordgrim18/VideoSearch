from django.urls import path, include

urlpatterns = [
    path("videos/", include("api.video.video_url")), # video urls
    path("subtitles/", include("api.subtitle.subtitle_url")), # subtitle urls
    path("storage/", include("api.storage.storage_url")), # storage urls

]