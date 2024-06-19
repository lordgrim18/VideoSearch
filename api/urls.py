from django.urls import path, include

urlpatterns = [
    path("videos/", include("api.video.video_urls")), # video urls
    path("subtitles/", include("api.subtitle.subtitle_urls")), # subtitle urls
    path("storage/", include("api.storage.storage_urls")), # storage urls

]