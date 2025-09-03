import os
from typing import Dict
from googleapiclient.http import MediaFileUpload
from src.logger import get_logger
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient import discovery
import pickle

logger = get_logger(__name__)

class YouTubeUploader:
    def __init__(self, client_secrets_file: str, scopes=None):
        if scopes is None:
            scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.client_secrets_file = client_secrets_file
        self.scopes = scopes
        self.youtube = None

    def authenticate(self) -> None:
        try:
            logger.info("Starting YouTube authentication process.")
            
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" #!Dikkat: Güvenli olmayan transport için, sadece geliştirme amaçlı
            
            creds = None
            token_file = 'youtube_token.pickle'
            
            if os.path.exists(token_file):
                logger.info("Loading existing credentials from token file.")
                with open(token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    logger.info("Refreshing expired credentials.")
                    creds.refresh(Request())
                else:
                    logger.info("No valid credentials found. Starting new authentication flow.")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.client_secrets_file, self.scopes
                    )
                    creds = flow.run_local_server(port=0)
                
                logger.info("Saving credentials to token file.")
                with open(token_file, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.youtube = discovery.build(
                "youtube", "v3", credentials=creds
            )
            logger.info("YouTube authentication successful.")
            
        except Exception as e:
            logger.error(f"Error during authentication: {e}")
            raise

    def upload_video(self, file_path: str, title: str, description: str = "", category_id: str = "22", privacy_status: str = "private") -> Dict:
        if self.youtube is None:
            raise RuntimeError("YouTube API client oluşturulmamış. Önce authenticate() çağırın.")
        try:
            logger.info(f"Uploading video {file_path} to YouTube.")
            request = self.youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description,
                        "categoryId": category_id
                    },
                    "status": {
                        "privacyStatus": privacy_status
                    }
                },
                media_body=MediaFileUpload(file_path)
            )

            response = request.execute()
            logger.info(f"Video uploaded successfully.")
        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            raise e
        return response

if __name__ == "__main__":
    uploader = YouTubeUploader(client_secrets_file="client_secret.json")
    uploader.authenticate()
    response = uploader.upload_video(
        file_path="artifacts/final_video.mp4",
        title="Test video upload",
        description="Description of uploaded video."
    )
    print(response)