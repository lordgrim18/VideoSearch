import uuid
from django.db import models

class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    video_file_name = models.FileField(upload_to='videos/')

class Subtitle(models.Model):
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    start_time = models.FloatField()
    text = models.TextField()
    text_lower = models.TextField()