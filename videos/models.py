import uuid
from django.db import models

class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')
    s3_url = models.URLField(blank=True, null=True)

class Subtitle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    start_time = models.FloatField()
    end_time = models.FloatField()
    text = models.TextField()