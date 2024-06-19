import boto3
from decouple import config
from rest_framework.views import APIView

from api.utils import CustomResponse
from .storage_serializer import StorageSerializer, StorageURLSerializer


class StorageListAPIView(APIView):

    def get(self, request):
        s3 = boto3.client('s3')
        bucket_name = config('BUCKET_NAME')
        bucket_objs = s3.list_objects_v2(Bucket=bucket_name)
        if bucket_objs.get('Contents') is None:
            return CustomResponse(message="No Objects found inside storage", data={}).failure_response()
        
        files = [{'object_name': file['Key']} for file in bucket_objs['Contents']]
        serializer = StorageSerializer(data=files, many=True)
        if serializer.is_valid():
            return CustomResponse(message="Storage objects fetched successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error fetching storage objects", data=serializer.errors).failure_response()

class StorageAPIView(APIView):

    def get(self, request, object_name):
        serializer = StorageSerializer(data={'object_name': object_name})
        if serializer.is_valid():
            download = serializer.retrieve(object_name)
            return download
        return CustomResponse(message="Error fetching object", data=serializer.errors).failure_response()

    def delete(self, request, object_name):
        serializer = StorageSerializer(data={'object_name': object_name})
        if serializer.is_valid():
            serializer.destroy(object_name)
            return CustomResponse(message="Object deleted successfully", data={}).success_response()
        return CustomResponse(message="Error deleting object", data=serializer.errors).failure_response()
    
class StorageURLAPIView(APIView):
    def get(self, request):
        serializer = StorageURLSerializer(data=request.data)
        if serializer.is_valid():
            return CustomResponse(message="Object URL generated successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error generating object URL", data=serializer.errors).failure_response()