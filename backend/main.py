from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from emotion_detecter import detect_emotion_from_frame
from music_mapper import get_tracks_for_emotion
import numpy as np
import cv2
from PIL import Image
import io

app = FastAPI(title="Emotion Music Player API")

# Allow React frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Check if API is running"""
    return {"status": "running", "message": "Emotion Music Player API is live!"}


@app.post("/detect-emotion")
async def detect_emotion(file: UploadFile = File(...)):
    """
    Accepts a webcam frame (image file)
    Returns detected emotion + confidence
    """
    try:
        # Read image bytes
        contents = await file.read()

        # Convert to numpy array for OpenCV
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        frame = np.array(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Detect emotion
        result = detect_emotion_from_frame(frame)

        return {
            "success": True,
            "emotion": result["emotion"],
            "confidence": result["confidence"],
            "all_emotions": result.get("all_emotions", {})
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/recommend-music/{emotion}")
def recommend_music(emotion: str, limit: int = 5):
    """
    Accepts an emotion string
    Returns list of YouTube tracks
    """
    try:
        result = get_tracks_for_emotion(emotion, limit=limit)

        if "error" in result:
            return {"success": False, "error": result["error"]}

        return {
            "success": True,
            "emotion": emotion,
            "tracks": result["tracks"]
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/emotions")
def get_supported_emotions():
    """Returns list of all supported emotions"""
    return {
        "emotions": [
            "happy", "sad", "angry",
            "neutral", "surprise", "fear", "disgust"
        ]
    }