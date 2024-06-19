import boto3
from rest_framework.views import APIView

from api.utils import CustomResponse
from core.dynamo_setup import video_table, subtitle_table
from .subtitle_serializer import VideoSubtitleSerializer

class SubtitleListAPIView(APIView):
    def get(self, request, video_id):
        subtitles = subtitle_table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('video_id').eq(video_id))
        if subtitles.get('Items') is None:
            return CustomResponse(message="No subtitles found", data={}).failure_response()
        
        count = len(subtitles['Items'])
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
            data = {
                'count': count,
                'results': serializer.data
            }
            return CustomResponse(message="Subtitles fetched successfully", data=serializer.data).success_response()
        return CustomResponse(message="Error fetching subtitles", data=serializer.errors).failure_response()
    
class SubtitleSearchAPIView(APIView):

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
    
class SubtitleVideoSearchAPIView(APIView):

        def get(self, request, video_id):
            keyword = request.query_params.get('keyword')
            if not keyword:
                return CustomResponse(message="No keyword provided", data={}).failure_response()
            
            video_title = video_table.get_item(Key={'id': video_id})['Item']['title']

            # subtitle_results = subtitle_table.query(
            #     KeyConditionExpression=boto3.dynamodb.conditions.Key('video_id').eq(video_id) & boto3.dynamodb.conditions.Key('text_lower').contains(keyword.lower())
            # )

            subtitle_results = subtitle_table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr('video_id').eq(video_id) & boto3.dynamodb.conditions.Attr('text_lower').contains(keyword.lower())
            )['Items']

            count = len(subtitle_results)

            subtitles = [{
                'start_time': str(subtitle['start_time']),
                'text': subtitle['text']
            } for subtitle in subtitle_results]
            data = {
                'video_id': video_id,
                'video_title': video_title,
                'subtitles': subtitles
            }

            serializer = VideoSubtitleSerializer(data=data)
            if serializer.is_valid():
                data = {
                    'keyword': keyword,
                    'count': count,
                    'results': serializer.data
                }
                return CustomResponse(message="Subtitles fetched successfully", data=data).success_response()
            return CustomResponse(message="Error fetching subtitles", data=serializer.errors).failure_response()
            