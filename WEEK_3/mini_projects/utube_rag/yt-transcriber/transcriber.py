from faster_whisper import WhisperModel

def load_model(model_name="small", compute_type="int8"):
    return WhisperModel(model_name, compute_type=compute_type)


def transcribe(model, audio_path):

    print("Started transcribing of videos...")

    segments, _ = model.transcribe(audio_path, beam_size=5)

    text = ""
    for seg in segments:
        print(f"[{seg.start:.2f}s → {seg.end:.2f}s] {seg.text}")
        text += seg.text + "\n"

    print("Completed transcribing of videos...")

    return text