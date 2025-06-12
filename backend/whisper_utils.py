import whisper
import os

# Load model once (cache globally)
model = whisper.load_model("base")  # Use "small" for better accuracy

def transcribe_audio(filepath):
    """Transcribe audio with optimized settings"""
    try:
        result = model.transcribe(
            filepath,
            fp16=False,  # Disable if running on CPU
            language="en",
            temperature=0.2  # Reduce randomness
        )
        return result["text"]
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {str(e)}")