import whisper
import os

model = whisper.load_model("base")  

def transcribe_audio(filepath):
    """Transcribe audio with optimized settings"""
    try:
        result = model.transcribe(
            filepath,
            fp16=False, 
            language="en",
            temperature=0.2
        )
        return result["text"]
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {str(e)}")