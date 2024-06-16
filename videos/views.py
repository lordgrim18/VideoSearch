from django.shortcuts import render, redirect
from .forms import VideoUploadForm
from .models import Video
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
