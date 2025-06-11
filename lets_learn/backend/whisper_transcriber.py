from faster_whisper import WhisperModel
import os

# Load Whisper (base model is fast and accurate for English)
WHISPER_MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large
whisper_model = WhisperModel(WHISPER_MODEL_SIZE, compute_type="int8")  # "int8" is good for CPU

UPLOAD_DIR = "../data/uploads/"

def transcribe_audio(file_path: str) -> str:
    """Transcribe audio file to text"""
    segments, info = whisper_model.transcribe(file_path)

    full_text = ""
    for segment in segments:
        full_text += segment.text + " "

    return full_text.strip()