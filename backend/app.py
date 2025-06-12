from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from whisper_utils import transcribe_audio
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Config
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

# Initialize OpenAI client
client = OpenAI(api_key="your-openai-key")  # Replace with your key

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

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a call center AI assistant. Provide short, actionable responses to the agent."},
                {"role": "user", "content": f"Conversation:\n{transcript}\n\nSuggested response:"}
            ],
            max_tokens=100
        )
        return jsonify({"suggestion": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)