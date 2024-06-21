import os
import boto3
from decouple import config
from django.conf import settings
from rest_framework import serializers

from api.utils import CustomResponse


class StorageSerializer(serializers.Serializer):
    object_name = serializers.CharField(required=True)

    def validate(self, data):
        object_name = data.get('object_name')
        s3 = boto3.client('s3')
        bucket_name = config('BUCKET_NAME')
        bucket_objs = s3.list_objects_v2(Bucket=bucket_name)

        if bucket_objs.get('Contents') is None:
            raise serializers.ValidationError('No Objects found inside storage')
        if object_name not in [file['Key'] for file in bucket_objs['Contents']]:
            raise serializers.ValidationError('Object not found in storage')
        return data

    def retrieve(self, object_name):
        s3 = boto3.client('s3')
        bucket_name = config('BUCKET_NAME')

        download_path = os.path.join(settings.MEDIA_ROOT, 'videos', object_name)
        if os.path.exists(download_path):
            return CustomResponse(message="File already exists", data={'download_path': download_path}).failure_reponse()
        
        s3.download_file(bucket_name, object_name, download_path)
        return CustomResponse(message="File downloaded successfully", data={'download_path': download_path}).success_response()
    
    # def destroy(self, object_name):
    #     s3 = boto3.client('s3')
    #     bucket_name = config('BUCKET_NAME')
    #     s3.delete_object(Bucket=bucket_name, Key=object_name)

class StorageURLSerializer(StorageSerializer):
    expires_in = serializers.IntegerField(required=False)
    presigned_url = serializers.SerializerMethodField()

    def validate(self, data):
        super().validate(data)
        expires_in = data.get('expires_in', 3600)
        data['expires_in'] = expires_in
        return data
    
    def get_presigned_url(self, validated_data):
        object_name = validated_data['object_name']
        expires_in = validated_data['expires_in']
        s3 = boto3.client('s3')
        bucket_name = config('BUCKET_NAME')
        url = s3.generate_presigned_url(
            'get_object', 
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expires_in
        )
        return url