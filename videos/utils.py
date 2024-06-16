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