from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("videos/", include("frontend.videos.video_front_urls")),
]