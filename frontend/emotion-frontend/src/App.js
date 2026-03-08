import React, { useState, useRef, useEffect, useCallback } from "react";
import Webcam from "react-webcam";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8080";

const EMOTION_EMOJIS = {
  happy: "😊",
  sad: "😢",
  angry: "😠",
  neutral: "😐",
  surprise: "😲",
  fear: "😨",
  disgust: "🤢",
};

const EMOTION_COLORS = {
  happy: "#FFD700",
  sad: "#6495ED",
  angry: "#FF4500",
  neutral: "#808080",
  surprise: "#FF69B4",
  fear: "#9370DB",
  disgust: "#32CD32",
};

export default function App() {
  const webcamRef = useRef(null);
  const [emotion, setEmotion] = useState("neutral");
  const [confidence, setConfidence] = useState(0);
  const [tracks, setTracks] = useState([]);
  const [isDetecting, setIsDetecting] = useState(false);
  const [loading, setLoading] = useState(false);

  const detectEmotion = useCallback(async () => {
    if (!webcamRef.current || loading) return;

    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) return;

    try {
      setLoading(true);

      // Convert base64 to blob
      const res = await fetch(imageSrc);
      const blob = await res.blob();

      // Send to backend
      const formData = new FormData();
      formData.append("file", blob, "frame.jpg");

      const response = await axios.post(`${API_URL}/detect-emotion`, formData);

      if (response.data.success) {
        const detectedEmotion = response.data.emotion;
        setEmotion(detectedEmotion);
        setConfidence(response.data.confidence);

        // Fetch music for detected emotion
        const musicResponse = await axios.get(
          `${API_URL}/recommend-music/${detectedEmotion}?limit=5`
        );
        if (musicResponse.data.success) {
          setTracks(musicResponse.data.tracks);
        }
      }
    } catch (error) {
      console.error("Detection error:", error);
    } finally {
      setLoading(false);
    }
  }, [loading]);

  // Auto detect every 5 seconds
  useEffect(() => {
    let interval;
    if (isDetecting) {
      detectEmotion(); // run immediately
      interval = setInterval(detectEmotion, 5000);
    }
    return () => clearInterval(interval);
  }, [isDetecting, detectEmotion]);

  const currentColor = EMOTION_COLORS[emotion] || "#808080";
  const currentEmoji = EMOTION_EMOJIS[emotion] || "😐";

  return (
    <div className="app" style={{ "--accent": currentColor }}>
      <h1 className="title">🎵 Emotion Music Player</h1>

      {/* Webcam Section */}
      <div className="webcam-container">
        <Webcam
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          className="webcam"
          mirrored={true}
        />
        <div className="emotion-badge" style={{ background: currentColor }}>
          {currentEmoji} {emotion.toUpperCase()} —{" "}
          {(confidence * 100).toFixed(1)}%
        </div>
      </div>

      {/* Controls */}
      <div className="controls">
        <button
          className={`btn ${isDetecting ? "btn-stop" : "btn-start"}`}
          onClick={() => setIsDetecting(!isDetecting)}
        >
          {isDetecting ? "⏹ Stop Detection" : "▶ Start Detection"}
        </button>
        <button className="btn btn-manual" onClick={detectEmotion}>
          📸 Detect Now
        </button>
      </div>

      {loading && <p className="loading">🔍 Detecting emotion...</p>}

      {/* Tracks Section */}
      {tracks.length > 0 && (
        <div className="tracks-container">
          <h2 style={{ color: currentColor }}>
            {currentEmoji} Songs for your mood
          </h2>
          <div className="tracks-list">
            {tracks.map((track, index) => (
              <a
                key={index}
                href={track.youtube_url}
                target="_blank"
                rel="noopener noreferrer"
                className="track-card"
              >
                <img
                  src={track.thumbnail}
                  alt={track.title}
                  className="track-thumb"
                />
                <div className="track-info">
                  <p className="track-title">{track.title}</p>
                  <p className="track-channel">{track.channel}</p>
                </div>
                <span className="play-icon">▶</span>
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}