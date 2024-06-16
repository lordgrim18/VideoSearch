import re


def time_to_seconds(time_str):
    h, m, s = map(float, time_str.replace(',', '.').split(':'))
    return h * 3600 + m * 60 + s

def parse_srt(srt_content):
    pattern = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n((?:.*(?:\n(?!\d+\n))*)*)")
    matches = pattern.findall(srt_content)

    subtitles = []
    for match in matches:
        subtitles.append({
            'start': time_to_seconds(match[1]),
            'end': time_to_seconds(match[2]),
            'text': match[3]
        })

    return subtitles

from django.db.models import Q
from .models import Subtitle

# def search_subtitle(video_id, keyword=None, start_time=None, end_time=None):
#     # Start with a query set filtered by video ID
#     query_set = Subtitle.objects.filter(video__video_id=video_id)

#     # Apply keyword filter if provided
#     if keyword:
#         query_set = query_set.filter(text__icontains=keyword)

#     # Apply time filters if provided
#     if start_time is not None and end_time is not None:
#         query_set = query_set.filter(Q(start_time__gte=start_time) & Q(end_time__lte=end_time))
#     elif start_time is not None:
#         query_set = query_set.filter(start_time__gte=start_time)
#     elif end_time is not None:
#         query_set = query_set.filter(end_time__lte=end_time)

#     # Return the filtered query set
#     return query_set