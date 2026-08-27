from faster_whisper import WhisperModel

def load_model(model_name="small", compute_type="int8"):
    return WhisperModel(model_name, compute_type=compute_type)


def transcribe(model, audio_path):
    segments, _ = model.transcribe(audio_path)

    text = ""
    for seg in segments:
        text += seg.text + "\n"

    return text