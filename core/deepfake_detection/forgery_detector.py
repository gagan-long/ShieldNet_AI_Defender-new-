from transformers import pipeline
import cv2
from core.deepfake_detection.forgery_detector import DeepfakeDetector
import os

class DeepfakeDetector:
    def __init__(self):
        self.model = pipeline(
            "image-classification", 
            model="elftsdmr/Deepfake-Detection-Model"
        )

    def analyze_frame(self, frame_path):
        result = self.model(frame_path)
        return {
            "is_fake": result[0]['label'] == 'FAKE',
            "confidence": result[0]['score']
        }

    def video_analysis(self, video_path, frame_interval=30):
        cap = cv2.VideoCapture(video_path)
        results = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % frame_interval == 0:
                frame_path = f"temp_frame_{int(cap.get(cv2.CAP_PROP_POS_FRAMES))}.jpg"
                cv2.imwrite(frame_path, frame)
                results.append(self.analyze_frame(frame_path))
        
        cap.release()
        return results

# Use environment variable for media path
MEDIA_PATH = os.getenv('MEDIA_PATH', 'core/deepfake_detection/sample_media')

detector = DeepfakeDetector()
results = detector.video_analysis(f'{MEDIA_PATH}/real_video.mp4')