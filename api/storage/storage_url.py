from django.urls import path

from .storage_view import StorageListAPIView, StorageAPIView, StorageURLAPIView

urlpatterns = [
    path("url/", StorageURLAPIView.as_view(), name="storage_url"), # psot - generate a presigned url for a file in bucket

    path("", StorageListAPIView.as_view(), name="storage"), # get - list all files in bucket 
    # path("delete/<str:object_name>/", StorageAPIView.as_view(), name="delete_file"), # delete - delete a file from bucket 
    path("<str:object_name>/", StorageAPIView.as_view(), name="file"), # get - download a file from bucket
]