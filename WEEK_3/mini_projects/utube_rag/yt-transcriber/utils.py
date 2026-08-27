import re


def extract_video_id(url):
    match = re.search(r"v=([^&]+)", url)
    return match.group(1) if match else "unknown"