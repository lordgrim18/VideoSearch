import uuid
import boto3
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import VideoUploadForm
from .models import Video, Subtitle
from .tasks import extract_subtitles
from .utils import save_file_locally
from .dynamo_setup import video_table, subtitle_table


def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # video = form.save()
            title = form.cleaned_data['title']
            video_file = request.FILES['video_file']
            print('video_file:', video_file)
            video_id = str(uuid.uuid4())
            video_file_url = save_file_locally(video_file, video_id)
            
            try:
                video_table.put_item(
                    Item={
                        'id': video_id,
                        'title': title,
                        'video_file_url': video_file_url
                    }
                )
            except Exception as e:
                print('Error:', e)
                return render(request, 'videos/upload.html', {'form': form, 'error': 'Error saving video to database'})
            finally:
                extract_subtitles.delay_on_commit(video_id)
            return redirect('upload_video')
    else:
        form = VideoUploadForm()
    return render(request, 'videos/upload.html', {'form': form})

def search_subtitles(request):
    keyword = request.GET.get('keyword')
    if keyword:
        results = [
                {
                    'video_title': subtitle.video.title,
                    'start_time': subtitle.start_time,
                    'text': subtitle.text,
                }
                for subtitle in Subtitle.objects.filter(text__icontains=keyword)
            ]
        print(results)
    else:
        results = []
    return render(request, 'videos/search.html', {'results': results})

def home(request):
    video_subtitles = []
    videos = video_table.scan()['Items']
    for video in videos:
        subtitles = subtitle_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('video_id').eq(video['id'])
        )['Items']
        video_subtitles.append((video, subtitles))
    print(video_subtitles)
    

    return render(request, 'videos/home.html', {'video_subtitles': video_subtitles})
