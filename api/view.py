import boto3
from rest_framework.views import APIView

from api.utils import CustomResponse
from core.dynamo_setup import video_table, subtitle_table
from api.subtitle.subtitle_serializer import VideoSubtitleSerializer
from api.video.video_serializer import VideoSerializer

class SearchAPIView(APIView):

    def get(self, request):
        keyword = request.query_params.get('keyword')
        if not keyword:
            return CustomResponse(message="No keyword provided", data={}).failure_response()

        video_results = video_table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('title_lower').contains(keyword.lower())
        )['Items']

        subtitle_results = subtitle_table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('text_lower').contains(keyword.lower())
        )['Items']
        
        video_count = len(video_results)
        subtitle_count = len(subtitle_results)

        videos = [{
            'id': video['id'],
            'title': video['title']
        } for video in video_results]

        video_serializer = VideoSerializer(data=videos, many=True, context={'request': request})
        if video_serializer.is_valid():
            video_data = video_serializer.data
        else:
            video_data = video_serializer.errors

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

        subtitles = list(video_subtitles.values())

        subtitle_serializer = VideoSubtitleSerializer(data=subtitles, many=True)
        if subtitle_serializer.is_valid():
            subtitle_data = subtitle_serializer.data
        else:
            subtitle_data = subtitle_serializer.errors

        data = {
            'keyword': keyword,
            'video_count': video_count,
            'video_results': video_data,
            'subtitle_count': subtitle_count,
            'subtitle_results': subtitle_data
        }
        return CustomResponse(message="Search results fetched successfully", data=data).success_response()