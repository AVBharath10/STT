# Call Center AI Assistant Dashboard (Prototype)

This project provides a prototype of a real-time (segmented) call center AI assistant dashboard. It transcribes audio from a microphone and provides AI-generated suggestions for the agent's next response, all powered by local open-source models to ensure privacy and avoid API costs.

**Note:** This is a prototype. While it aims for near real-time suggestions, the transcription currently processes recorded segments after they are captured, rather than streaming word-by-word.

## ✨ Features

* **Microphone Audio Recording:** Capture audio directly from your browser's microphone.
* **Speech-to-Text (STT):** Transcribes recorded audio segments into text using a local Whisper model.
* **AI-Powered Suggestions:** Generates concise, actionable suggestions for call agents based on the transcript, using a local Large Language Model (LLM) via Ollama.
* **Frontend (React.js):** Intuitive user interface for recording and viewing transcripts/suggestions.
* **Backend (Flask):** Handles audio processing, STT, and communication with the local LLM.

## 🚀 Technologies Used

* **Frontend:**
    * React.js
    * Web Audio API (`MediaRecorder`)
* **Backend:**
    * Python 3
    * Flask
    * `openai-whisper`: For local Speech-to-Text inference.
    * `requests`: For communication with the local Ollama server.
* **Local LLM Runtime:**
    * [Ollama](https://ollama.com/): Runs large language models locally on your machine.
    * [Llama 3](https://ollama.com/library/llama3) (or other chosen LLM like Gemma, DeepSeek): The specific LLM model generating suggestions.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

* **Node.js & npm:** [Download & Install Node.js](https://nodejs.org/en/download/) (npm comes with it).
* **Python 3.8+:** [Download & Install Python](https://www.python.org/downloads/).
* **pip:** Python's package installer (comes with Python 3.4+).
* **Ollama:** [Download & Install Ollama](https://ollama.com/download) for your operating system.
* **ffmpeg:** This is required by the Whisper library for audio processing.
    * **Windows:** [Download from gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and add to your system's PATH.
    * **macOS:** `brew install ffmpeg` (if you have Homebrew).
    * **Linux:** `sudo apt update && sudo apt install ffmpeg` (Debian/Ubuntu) or equivalent for your distribution.

## ⚙️ Setup Instructions

Follow these steps to get the project up and running on your local machine.

**1. Clone the Repository**

```bash
git clone <YOUR_REPOSITORY_URL_HERE>
cd <your-project-folder-name>
