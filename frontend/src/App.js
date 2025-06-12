import React, { useState, useRef } from "react";
import { motion } from "framer-motion";
import "./App.css";

const App = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // ✅ Send audio to Whisper backend
  const sendAudioToBackend = async (audioBlob) => {
    const formData = new FormData();
    formData.append("file", audioBlob);

    try {
      setIsLoading(true);
      const response = await fetch("http://localhost:5000/transcribe", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setTranscript(data.text || "❌ Transcription failed");
    } catch (error) {
      console.error("API error:", error);
      setTranscript("❌ Network error");
    } finally {
      setIsLoading(false);
    }
  };

  // 🎤 Start microphone recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (e) => {
        audioChunksRef.current.push(e.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
        sendAudioToBackend(audioBlob);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setTranscript("🎙️ Recording...");

      // Send chunks every 2 seconds for near-real-time
      setInterval(() => {
        if (mediaRecorderRef.current?.state === "recording") {
          mediaRecorderRef.current.requestData();
        }
      }, 2000);

    } catch (error) {
      console.error("Microphone error:", error);
      setTranscript("❌ Microphone access denied");
    }
  };

  // ⏹️ Stop recording
  const stopRecording = () => {
    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
      setTranscript("⏳ Processing audio...");
    }
  };

  // 🤖 Generate AI suggestion
  const generateSuggestion = async () => {
    if (!transcript.trim()) return;

    try {
      setIsLoading(true);
      const response = await fetch("http://localhost:5000/generate_suggestion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript }),
      });
      const data = await response.json();
      setSuggestions([...suggestions, data.suggestion]);
    } catch (error) {
      console.error("Suggestion error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // 📁 Handle file upload
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setTranscript("⏳ Processing uploaded file...");
      sendAudioToBackend(file);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Call Intelligence Dashboard</h1>
        <div className="divider"></div>
      </header>

      <div className="dashboard-grid">
        {/* 🎤 Audio Control Panel */}
        <motion.div className="control-panel card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <h2>Audio Input</h2>
          <div className="button-group">
            <motion.button
              className="upload-btn"
              whileHover={{ scale: 1.05 }}
              onClick={() => document.getElementById("file-upload").click()}
            >
              📁 Upload Audio
            </motion.button>
            <input id="file-upload" type="file" hidden accept="audio/*" onChange={handleFileUpload} />

            {!isRecording ? (
              <motion.button
                className="record-btn"
                whileHover={{ scale: 1.05 }}
                onClick={startRecording}
              >
                🎤 Start Recording
              </motion.button>
            ) : (
              <motion.button
                className="stop-btn"
                whileHover={{ scale: 1.05 }}
                onClick={stopRecording}
              >
                ⏹️ Stop Recording
              </motion.button>
            )}
          </div>
        </motion.div>

        {/* 📝 Transcript Panel */}
        <motion.div className="transcript-panel card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <div className="panel-header">
            <h2>Live Transcript</h2>
            <motion.button
              className={`generate-btn ${isLoading ? "loading" : ""}`}
              whileHover={{ scale: 1.05 }}
              onClick={generateSuggestion}
              disabled={!transcript || isLoading}
            >
              {isLoading ? "⚡ Generating..." : "💡 Get Suggestion"}
            </motion.button>
          </div>
          <div className="transcript-content">
            {transcript ? (
              transcript.split('\n').map((line, i) => (
                <p key={i} className={line.startsWith("Agent:") ? "agent-line" : "customer-line"}>
                  {line}
                </p>
              ))
            ) : (
              <p className="placeholder">No transcript yet. Record or upload audio.</p>
            )}
          </div>
        </motion.div>

        {/* 🤖 Suggestions Panel */}
        <motion.div className="suggestions-panel card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <h2>AI Suggestions</h2>
          <div className="suggestions-list">
            {suggestions.length > 0 ? (
              suggestions.map((text, i) => (
                <motion.div
                  key={i}
                  className="suggestion-item"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  {text}
                </motion.div>
              ))
            ) : (
              <p className="placeholder">Suggestions will appear here</p>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default App;