from rest_framework import serializers


class SubtitleSerializer(serializers.Serializer):
    start_time = serializers.DecimalField(max_digits=10, decimal_places=3)
    text = serializers.CharField()

class VideoSubtitleSerializer(serializers.Serializer):
    video_id = serializers.CharField()
    video_title = serializers.CharField()
    subtitles = SubtitleSerializer(many=True)