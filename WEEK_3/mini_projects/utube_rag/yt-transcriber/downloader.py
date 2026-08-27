import subprocess
import os

def download_audio(url, audio_dir):
    print("Downloading audio...")

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

    # get latest downloaded file
    files = [f for f in os.listdir(audio_dir) if f.endswith(".mp3")]
    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(audio_dir, x)))

    print("Download completed")

    return os.path.join(audio_dir, latest_file)


def split_audio(audio_path, chunk_dir, chunk_length=75):
    print("Splitting audio into chunks...")

    os.makedirs(chunk_dir, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-i", audio_path,
        "-f", "segment",
        "-segment_time", str(chunk_length),
        "-c", "copy",
        f"{chunk_dir}/chunk_%03d.mp3"
    ]

    subprocess.run(cmd, check=True)

    chunks = sorted([
        os.path.join(chunk_dir, f)
        for f in os.listdir(chunk_dir)
        if f.endswith(".mp3")
    ])

    print(f" Created {len(chunks)} chunks")

    return chunks