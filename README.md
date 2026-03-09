# 🎵 Emotion Music Player

An AI-powered music player that detects your facial emotion in real-time using a webcam and automatically recommends YouTube music that matches your mood.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-orange?style=flat-square&logo=tensorflow)
![YouTube API](https://img.shields.io/badge/YouTube-Data%20API%20v3-red?style=flat-square&logo=youtube)

---

## 🚀 Demo

> 📸 Webcam captures your face → 🧠 CNN detects your emotion → 🎵 YouTube music plays automatically

---

## ✨ Features

- 🎭 **Real-time emotion detection** using CNN (FER library + TensorFlow)
- 🎵 **YouTube music recommendations** based on detected emotion
- 😊 Supports **7 emotions**: Happy, Sad, Angry, Neutral, Surprise, Fear, Disgust
- 🌈 **Dynamic UI** — color theme changes based on your current emotion
- ⚡ **Auto-detection** every 5 seconds with manual trigger option
- 🖥️ Clean dark-themed **React frontend**
- 🔗 Direct YouTube links with thumbnail previews

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Emotion Detection | OpenCV + FER (CNN-based) |
| Backend | FastAPI + Python |
| Music Recommendations | YouTube Data API v3 |
| Frontend | React.js |
| Deployment | Render (Backend) + Vercel (Frontend) |

---

## 📁 Project Structure

```
emotion-music-player/
│
├── backend/
│   ├── emotion_detecter.py    # Webcam + FER emotion detection
│   ├── music_mapper.py        # YouTube API music recommendations
│   └── main.py                # FastAPI REST API
│
├── frontend/
│   └── emotion-frontend/      # React.js UI
│       ├── src/
│       │   ├── App.js
│       │   └── App.css
│       └── package.json
│
├── requirements.txt
├── runtime.txt
├── Procfile
└── .gitignore
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 16+
- YouTube Data API v3 key

### 1. Clone the Repository
```bash
git clone https://github.com/captainTushar/emotion-music-player.git
cd emotion-music-player
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
YOUTUBE_API_KEY=your_youtube_api_key
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=http://127.0.0.1:3000/callback
```

### 4. Run the Backend
```bash
cd backend
uvicorn main:app --reload --port 8080
```

Backend will be live at: `http://127.0.0.1:8080`

### 5. Frontend Setup
```bash
cd frontend/emotion-frontend
npm install
npm start
```

Frontend will be live at: `http://localhost:3000`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check API status |
| POST | `/detect-emotion` | Send webcam frame → get emotion |
| GET | `/recommend-music/{emotion}` | Get YouTube tracks by emotion |
| GET | `/emotions` | List all supported emotions |

### Example Response — `/recommend-music/happy`
```json
{
  "success": true,
  "emotion": "happy",
  "tracks": [
    {
      "title": "Pharrell Williams - Happy",
      "channel": "PharrellWilliamsVEVO",
      "video_id": "ZbZSe6N_BXs",
      "thumbnail": "https://...",
      "youtube_url": "https://www.youtube.com/watch?v=ZbZSe6N_BXs"
    }
  ]
}
```

---

## 🎭 Emotion → Music Mapping

| Emotion | Music Style |
|---------|------------|
| 😊 Happy | Upbeat Pop |
| 😢 Sad | Lo-fi / Acoustic |
| 😠 Angry | Metal / Rap |
| 😐 Neutral | Jazz / Ambient |
| 😲 Surprise | Electronic |
| 😨 Fear | Classical |
| 🤢 Disgust | Indie / Alternative |

---

## 📊 Model Performance

- **Library:** FER (Facial Expression Recognition)
- **Architecture:** CNN-based deep learning model
- **Emotions Classified:** 7
- **Detection Interval:** Every 5 seconds (CPU optimized)
- **Inference Mode:** CPU (no GPU required)

---


## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Tushar Kandpal**
- GitHub: [@captainTushar](https://github.com/captainTushar)
- LinkedIn: [Tushar Kandpal](https://www.linkedin.com/in/tushar-kandpal-a9211919b/)

---

⭐ If you found this project helpful, please give it a star!
