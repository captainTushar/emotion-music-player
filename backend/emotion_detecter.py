import cv2
from fer import FER
import time

# Initialize detector
detector = FER(mtcnn=False)  # mtcnn=False is faster on CPU

def detect_emotion_from_frame(frame):
    """
    Takes a single frame, returns dominant emotion + confidence
    """
    result = detector.detect_emotions(frame)

    if not result:
        return {"emotion": "neutral", "confidence": 0.0}

    # Get the first detected face
    emotions = result[0]["emotions"]

    # Find dominant emotion
    dominant_emotion = max(emotions, key=emotions.get)
    confidence = round(emotions[dominant_emotion], 2)

    return {
        "emotion": dominant_emotion,
        "confidence": confidence,
        "all_emotions": emotions
    }


def run_webcam_detection():
    """
    Real-time webcam emotion detection
    Throttled to every 3 seconds to save CPU
    """
    cap = cv2.VideoCapture(0)  # 0 = default webcam

    if not cap.isOpened():
        print("❌ Cannot access webcam")
        return

    print("✅ Webcam started. Press 'q' to quit.")

    last_detection_time = 0
    current_emotion = "neutral"
    confidence = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break

        current_time = time.time()

        # Throttle: detect every 3 seconds
        if current_time - last_detection_time >= 3:
            result = detect_emotion_from_frame(frame)
            current_emotion = result["emotion"]
            confidence = result["confidence"]
            last_detection_time = current_time
            print(f"Detected: {current_emotion} ({confidence * 100:.1f}%)")

        # Display on frame
        label = f"{current_emotion.upper()} ({confidence * 100:.1f}%)"
        cv2.putText(frame, label, (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        cv2.imshow("Emotion Detector", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_webcam_detection()