import boto3
from decouple import config
from rest_framework.views import APIView

from api.utils import CustomResponse
from core.dynamo_setup import video_table, subtitle_table
from core.tasks import delete_video_subtitles

from .serializer import VideoSerializer, VideoSubtitleSerializer, StorageSerializer, StorageURLSerializer


class VideoListAPIView(APIView):
    def get(self, request):
        videos = video_table.scan()['Items']
        serializer = VideoSerializer(data=videos, many=True)
        if serializer.is_valid():
            return CustomResponse(message="Videos fetched successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error fetching videos", data=serializer.errors).failure_response()  

class VideoAPIView(APIView):

    def get(self, request, video_id):
        video = video_table.get_item(Key={'id': video_id})
        if video.get('Item') is None:
            return CustomResponse(message="Video not found", data={}).failure_response()
        serializer = VideoSerializer(data=video['Item'])
        if serializer.is_valid():
            return CustomResponse(message="Video fetched successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error fetching video", data=serializer.errors).failure_response()
        
    def post(self, request):
        serializer = VideoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="Video created successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error creating video", data=serializer.errors).failure_response()
    
    def patch(self, request, video_id):
        video = video_table.get_item(Key={'id': video_id})
        if video.get('Item') is None:
            return CustomResponse(message="Video not found", data={}).failure_response()
        serializer = VideoSerializer(video['Item'], data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message="Video updated successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error updating video", data=serializer.errors).failure_response()
    
    def delete(self, request, video_id):
        video = video_table.get_item(Key={'id': video_id})
        if video.get('Item') is None:
            return CustomResponse(message="Video not found", data={}).failure_response()
        delete_video_subtitles.delay(video_id)
        return CustomResponse(message="Video deleted successfully", data={}).success_response()
    
class SubtitleListAPIView(APIView):
    def get(self, request, video_id):
        subtitles = subtitle_table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('video_id').eq(video_id))
        if subtitles.get('Items') is None:
            return CustomResponse(message="No subtitles found", data={}).failure_response()
        
        video_title = video_table.get_item(Key={'id': video_id})['Item']['title']
        
        subtitles = [{
            'start_time': str(subtitle['start_time']),
            'text': subtitle['text']
        } for subtitle in subtitles['Items']]
        data = {
            'video_id': video_id,
            'video_title': video_title,
            'subtitles': subtitles
        }

        serializer = VideoSubtitleSerializer(data=data)
        if serializer.is_valid():
            return CustomResponse(message="Subtitles fetched successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error fetching subtitles", data=serializer.errors).failure_response()
    
class SubtitleAPIView(APIView):

    def get(self, request):
        keyword = request.query_params.get('keyword')
        if not keyword:
            return CustomResponse(message="No keyword provided", data={}).failure_response()

        subtitle_results = subtitle_table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('text_lower').contains(keyword.lower())
        )['Items']
        
        count = len(subtitle_results)
        video_subtitles = {}

        for subtitle in subtitle_results:
            video_id = subtitle['video_id']
            video = video_table.get_item(Key={'id': video_id}).get('Item')

            if video:
                if video_id not in video_subtitles:
                    video_subtitles[video_id] = {
                        'video_id': video_id,
                        'video_title': video['title'],
                        'subtitles': []
                    }
                video_subtitles[video_id]['subtitles'].append({
                    'start_time': subtitle['start_time'],
                    'text': subtitle['text']
                })

        results = list(video_subtitles.values())

        serializer = VideoSubtitleSerializer(data=results, many=True)
        if serializer.is_valid():
            data = {
                'keyword': keyword,
                'count': count,
                'results': serializer.data
            }
            return CustomResponse(message="Subtitles fetched successfully", data=data).success_response()
        return CustomResponse(message="Error fetching subtitles", data=serializer.errors).failure_response()
    
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