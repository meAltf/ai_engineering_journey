import subprocess
import os

def download_audio(url, audio_dir):

    print("Started downloading videos...")

    os.makedirs(audio_dir, exist_ok=True)

    output_template = os.path.join(audio_dir, "%(title)s.%(ext)s")

    subprocess.run([
        "yt-dlp",
        "--no-playlist",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", output_template,
        url
    ], check=True)

    # return latest file (simple approach)
    files = os.listdir(audio_dir)
    files = [f for f in files if f.endswith(".mp3")]
    
    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(audio_dir, x)))
    print("Completed downloading videos...")

    return os.path.join(audio_dir, latest_file)