import requests
import time
import os
from dotenv import load_dotenv
from src.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

class DIDVideoGenerator:
    def __init__(self):
        self.api_key = os.getenv('DID_API_KEY')
        self.api_url = "https://api.d-id.com/talks"
        self.source_url = "https://d-id-public-bucket.s3.us-west-2.amazonaws.com/alice.jpg"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }

    def create_video(self, audio_url: str, fluent: bool = False) -> str:
        try:
            logger.info("Creating video with DID API")
            payload = {
                "source_url": self.source_url,
                "script": {
                    "type": "audio",
                    "subtitles": False,
                    "audio_url": audio_url
                },
                "config": { "fluent": str(fluent).lower() }
            }

            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()
            video_id = response.json()["id"]
            logger.info(f"Video created with ID: {video_id}")
            print("Video ID:", video_id)
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            raise e
        return video_id

    def wait_for_video(self, video_id, poll_interval=5):
        try:
            logger.info(f"Waiting for video {video_id} to be ready")
            video_url = f"{self.api_url}/{video_id}"

            while True:
                response = requests.get(video_url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                status = data.get("status")
                print("Current status:", status)

                if status == "done":
                    logger.info(f"Video {video_id} is ready")
                    print("Video hazır!")
                    return data.get("result_url")
                elif status in ["error", "rejected"]:
                    logger.error(f"Video {video_id} creation failed with status: {status}")
                    raise Exception(f"Video oluşturulamadı: {status}")
                else:
                    logger.info(f"Video {video_id} status: {status}. Checking again in {poll_interval} seconds.")
                    time.sleep(poll_interval)
        except Exception as e:
            logger.error(f"Error waiting for video: {e}")
            raise e
        
        
if __name__ == "__main__":
    generator = DIDVideoGenerator()

    audio_file_url = "https://storage.googleapis.com/ai-audio-bucket/output1.mp3"

    video_id = generator.create_video(audio_file_url)
    video_url = generator.wait_for_video(video_id)
    print("Video URL:", video_url)
