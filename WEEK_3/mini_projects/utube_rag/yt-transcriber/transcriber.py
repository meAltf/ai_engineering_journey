from faster_whisper import WhisperModel
import json


def load_model(model_name="small", compute_type="int8"):
    print("Loading Whisper model...")
    return WhisperModel(model_name, compute_type=compute_type)


def transcribe_chunks(model, chunks, video_id):
    print("Transcribing chunks...")

    results = []

    for i, chunk in enumerate(chunks):
        start_time = i * 75
        end_time = start_time + 75

        print(f"Processing chunk {i+1} ({start_time}s - {end_time}s)")

        segments, _ = model.transcribe(chunk)

        text = " ".join([seg.text for seg in segments]).strip()

        results.append({
            "video_id": video_id,
            "start": start_time,
            "end": end_time,
            "text": text
        })

    print("Transcription completed")

    return results


def save_json(data, output_path):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved JSON: {output_path}")