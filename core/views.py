import uuid
import boto3
from django.shortcuts import render, redirect

from .forms import VideoUploadForm
from .tasks import extract_subtitles
from .utils import save_file_locally
from .dynamo_setup import video_table, subtitle_table


def home(request):
    video_subtitles = []
    videos = video_table.scan()['Items']
    for video in videos:
        subtitles = subtitle_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('video_id').eq(video['id'])
        )['Items']
        video_subtitles.append((video, subtitles))
    return render(request, 'core/home.html', {'video_subtitles': video_subtitles})

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            video_file = request.FILES['video_file']
            video_id = str(uuid.uuid4())
            video_file_name = f"{video_id}_{video_file.name}"
            local_file_url = save_file_locally(video_file, video_file_name)            
            try:
                video_table.put_item(
                    Item={
                        'id': video_id,
                        'title': title,
                        'video_file_name': video_file_name
                    }
                )
            except Exception as e:
                print('Error:', e)
                return render(request, 'videos/upload.html', {'form': form, 'error': 'Error saving video to database'})
            finally:
                extract_subtitles.delay_on_commit(video_id, local_file_url, video_file_name)
            return redirect('upload_video')
    else:
        form = VideoUploadForm()
    return render(request, 'core/upload.html', {'form': form})

def search_subtitles(request):
    keyword = request.GET.get('keyword')
    results = []
    if keyword:
        subtitle_results = subtitle_table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('text_lower').contains(keyword.lower())
        )['Items']

        for subtitle in subtitle_results:
            video = video_table.get_item(Key={'id': subtitle['video_id']})['Item']
            results.append({
                'video_title': video['title'],
                'video_id': subtitle['video_id'],
                'start_time': subtitle['start_time'],
                'text': subtitle['text']
            })
    return render(request, 'core/search.html', {'results': results})