from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# YouTube API setup
api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=api_key)

# Emotion to search query mapping
EMOTION_MUSIC_MAP = {
    "happy":    "happy upbeat pop music",
    "sad":      "sad lofi acoustic music",
    "angry":    "aggressive metal rap music",
    "neutral":  "chill jazz ambient music",
    "surprise": "energetic electronic music",
    "fear":     "calming classical music",
    "disgust":  "indie alternative music"
}


def get_tracks_for_emotion(emotion: str, limit: int = 5):
    """
    Takes an emotion string, returns a list of YouTube tracks
    """
    query = EMOTION_MUSIC_MAP.get(emotion.lower(), "chill ambient music")

    try:
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            videoCategoryId="10",  # Music category
            maxResults=limit
        )
        response = request.execute()

        tracks = []
        for item in response["items"]:
            track = {
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "video_id": item["id"]["videoId"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "youtube_url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            tracks.append(track)

        return {"emotion": emotion, "tracks": tracks}

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Test with all emotions
    test_emotions = ["happy", "sad", "angry", "neutral", "surprise", "fear", "disgust"]

    for emotion in test_emotions:
        print(f"\n🎵 Emotion: {emotion.upper()}")
        result = get_tracks_for_emotion(emotion, limit=3)

        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            for track in result["tracks"]:
                print(f"  🎵 {track['title']} — {track['channel']}")
                print(f"     🔗 {track['youtube_url']}")