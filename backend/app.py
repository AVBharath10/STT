from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from whisper_utils import transcribe_audio
import requests 

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg','webm'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        transcript = transcribe_audio(filepath)
        return jsonify({"text": transcript})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/generate_suggestion', methods=['POST'])
def generate_suggestion():
    data = request.json
    transcript = data.get("transcript", "")

    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400

    OLLAMA_API_URL = "http://localhost:11434/api/generate"
    OLLAMA_MODEL = "llama3" # <-- CHANGE THIS if your model is named differently (e.g., "llama3:8b")

    prompt_text = f"""
       You are a helpful call center AI assistant. Your ONLY task is to provide the agent with a concise, actionable, and natural-sounding response to the customer based on the conversation transcript. DO NOT include any introductory or concluding remarks about your process or the suggestion itself. Just provide the direct agent response. Focus on the most immediate next step or information needed.
    Conversation Transcript:
    {transcript}

    Agent's Next Suggested Response:
    """

    try:
        # Send request to Ollama API
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt_text,
                "stream": False,  # We want a single response, not a stream of tokens
                "options": {
                    "temperature": 0.7, # Adjust as needed (0.0 for deterministic, 1.0 for more creative)
                    "num_predict": 128, # Max tokens in the response (adjust based on desired length)
                    "top_k": 40,
                    "top_p": 0.9
                }
            }
        )
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        ollama_response = response.json()
        # The actual text content is usually in the 'response' field for /api/generate
        suggestion = ollama_response.get("response", "No suggestion generated.")

        return jsonify({"suggestion": suggestion})

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
        return jsonify({"error": f"Failed to get suggestion from Ollama: {e}"}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)