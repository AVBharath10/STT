all Center AI Assistant Dashboard (Prototype)
This project provides a prototype of a real-time (segmented) call center AI assistant dashboard. It transcribes audio from a microphone and provides AI-generated suggestions for the agent's next response, all powered by local open-source models to ensure privacy and avoid API costs.

Note: This is a prototype. While it aims for near real-time suggestions, the transcription currently processes recorded segments after they are captured, rather than streaming word-by-word.

✨ Features
Microphone Audio Recording: Capture audio directly from your browser's microphone.
Speech-to-Text (STT): Transcribes recorded audio segments into text using a local Whisper model.
AI-Powered Suggestions: Generates concise, actionable suggestions for call agents based on the transcript, using a local Large Language Model (LLM) via Ollama.
Frontend (React.js): Intuitive user interface for recording and viewing transcripts/suggestions.
Backend (Flask): Handles audio processing, STT, and communication with the local LLM.
🚀 Technologies Used
Frontend:
React.js
Web Audio API (MediaRecorder)
Backend:
Python 3
Flask
openai-whisper: For local Speech-to-Text inference.
requests: For communication with the local Ollama server.
Local LLM Runtime:
Ollama: Runs large language models locally on your machine.
Llama 3 (or other chosen LLM like Gemma, DeepSeek): The specific LLM model generating suggestions.
📋 Prerequisites
Before you begin, ensure you have the following installed:

Node.js & npm: Download & Install Node.js (npm comes with it).
Python 3.8+: Download & Install Python.
pip: Python's package installer (comes with Python 3.4+).
Ollama: Download & Install Ollama for your operating system.
ffmpeg: This is required by the Whisper library for audio processing.
Windows: Download from gyan.dev and add to your system's PATH.
macOS: brew install ffmpeg (if you have Homebrew).
Linux: sudo apt update && sudo apt install ffmpeg (Debian/Ubuntu) or equivalent for your distribution.
⚙️ Setup Instructions
Follow these steps to get the project up and running on your local machine.

1. Clone the Repository

Bash

git clone https://github.com/AVBharath10/STT
cd STT # IMPORTANT: Change into the cloned repository's root directory 2. Backend Setup (Flask & Python)

Navigate into the backend directory from the project root:

Bash

cd backend
Create a Python virtual environment (highly recommended):

Bash

python -m venv venv
Activate the virtual environment:

Windows:
Bash

.\venv\Scripts\activate
macOS / Linux:
Bash

source venv/bin/activate
Install the required Python packages:

Bash

pip install Flask Flask-Cors Werkzeug openai-whisper requests
(Optional: If you plan to manage sensitive keys or configs for future additions, you might also pip install python-dotenv and use a .env file for best practices, but it's not strictly required for Ollama's local setup.)

Important for Whisper Model:
The whisper_utils.py file defaults to the "base" Whisper model for better performance on laptops. The first time you run the Flask app, this model will download automatically (approx. 139MB). If you wish to try a more accurate (but larger/slower) model like "small" (approx. 461MB) or "medium" (approx. 1.4GB), modify the line in whisper_utils.py:
model = whisper.load_model("base") to model = whisper.load_model("small") or model = whisper.load_model("medium").

3. Ollama & Local LLM Setup

You need to set up Ollama and pull the desired Large Language Model (LLM).

Start Ollama Server:
In a separate terminal window, start the Ollama server. This terminal must remain open as long as you want to use Ollama.

Bash

ollama serve
If you see an error like bind: Only one usage of each socket address..., it means Ollama is already running in the background. You can usually confirm by visiting http://localhost:11434/ in your browser.

Pull the LLM:
Pull the Llama 3 model (or another model like gemma3:1b if Llama 3 is too heavy for your machine). For Llama 3, the 8b (8 billion parameter) variant is commonly pulled.

Bash

ollama pull llama3 # This usually pulls llama3:8b by default, approx. 4.7GB

# OR if your laptop struggles, try a smaller model like:

# ollama pull gemma3:1b # Approx. 815MB

# ollama pull deepseek-r1:1.5b # Approx. 1.1GB

4. Frontend Setup (React)

First, navigate back to the root of your project:

Bash

cd ..
Then, navigate into the frontend directory:

Bash

cd frontend
Install the Node.js dependencies:

Bash

npm install
▶️ Running the Project
You will need three separate terminal windows open: one for Ollama, one for the Flask backend, and one for the React frontend.

Terminal 1: Start Ollama Server

Bash

ollama serve
(Ensure this is running and accessible at http://localhost:11434)

Terminal 2: Start Flask Backend
Navigate to your backend directory, activate your virtual environment, and run the Flask app:

Bash

cd backend
.\venv\Scripts\activate # Windows

# OR

# source venv/bin/activate # macOS/Linux

python app.py
You should see output indicating the Flask server is running on http://0.0.0.0:5000.

Terminal 3: Start React Frontend
Navigate to your frontend directory and start the React development server:

Bash

cd frontend
npm start
This will usually open your browser automatically to http://localhost:3000.

🎤 Usage
Allow microphone access when prompted by your browser.
Click the "Start Recording" button.
Speak into your microphone.
Click "Stop Recording". The audio segment will be sent to the backend for transcription.
Once transcribed, the text will appear. You can then request a suggestion for the agent's next response based on that transcript.
⚠️ Important Considerations & Troubleshooting
Microphone Permissions: Ensure your browser and operating system have granted microphone access to localhost.
Resource Usage: Running LLMs locally, especially larger ones (Llama 3 8B, Whisper Medium), consumes significant RAM and CPU.
If your laptop struggles, consider using smaller models (gemma3:1b, deepseek-r1:1.5b for LLM; base, small for Whisper).
Close other demanding applications while running the project.
Transcription Accuracy:
Depends heavily on the Whisper model size (base is fastest but least accurate; small is a good balance).
Crucially, depends on your microphone quality and the clarity of your audio input. Minimize background noise!
Ollama Model Choice: The quality of AI suggestions directly correlates with the size and capability of the LLM you choose (e.g., Llama 3 is more capable than Gemma 1B).
ffmpeg: Ensure ffmpeg is correctly installed and its path is accessible by your Python environment for Whisper to function.
Port Conflicts: If ollama serve fails, another process might be using port 11434. If Flask fails, another process might be using port 5000.
Real-time vs. Segmented: This prototype currently processes audio in segments after recording stops. Achieving true word-by-word real-time transcription requires a more complex architecture (e.g., WebSockets for continuous audio streaming), which is beyond the scope of this initial prototype but a valuable future enhancement.
