from rest_framework import serializers

from core.models import Video, Subtitle
from core.dynamo_setup import video_table, subtitle_table

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'