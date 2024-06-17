from django.shortcuts import render, redirect
from .forms import VideoUploadForm
from .models import Video, Subtitle
from .tasks import extract_subtitles

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            extract_subtitles.delay_on_commit(video.id)   
            # extract_subtitles(video.id)
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
                    'end_time': subtitle.end_time,
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
    videos = Video.objects.all()
    for video in videos:
        subtitles = Subtitle.objects.filter(video=video)
        video_subtitles.append((video, subtitles))

    return render(request, 'videos/home.html', {'video_subtitles': video_subtitles})
