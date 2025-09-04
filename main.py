from src.news_fetcher import NewsFetcher
from src.text_to_speech import ElevenLabsTTS
from src.did_video import DIDVideoGenerator
from src.gcs_uploader import GCSUploader
from src.youtube_uploader import YouTubeUploader
from src.text_editor import text_editor
from src.credit_tracker import CreditTracker
from src.smtp_sender import EmailSender
from src.logger import get_logger
import datetime
import asyncio
import time

from utils.common_functions import download_video, load_config

def main():
    start_time = time.time()
    logger = get_logger(__name__)
    
    logger.info("👌 Pipeline started.")
    print("👌 Pipeline started.")
    
    configs = load_config("config/config.yaml")
    
    news_fetcher = NewsFetcher()
    news = news_fetcher.fetch_news_content(news_count=2)
    print("News fetched successfully.")
    
    edited_news = asyncio.run(text_editor(news))
    print("News edited successfully.")

    tts_client = ElevenLabsTTS()
    audio_file = tts_client.text_to_speech(
        text=edited_news,
        filename=configs["audio_file"],
    )
    print("Audio file created successfully.")

    gcs_uploader = GCSUploader(bucket_name=configs["bucket_name"])
    public_url = gcs_uploader.upload_file(audio_file)
    print("Audio file uploaded to GCS successfully.")

    did_client = DIDVideoGenerator()
    video_id = did_client.create_video(audio_url=public_url)
    created_url = did_client.wait_for_video(video_id)
    print("Video created successfully.")
    
    credit_tracker = CreditTracker()
    credit_tracker.save_to_db()
    print("Credit usage saved to database successfully.")

    download_video(created_url, configs["video_file"])
    print("Video downloaded successfully.")

    youtube_uploader = YouTubeUploader(client_secrets_file=configs["client_secret_file"])
    youtube_uploader.authenticate()
    youtube_uploader.upload_video(file_path=configs["video_file"], title=f"{datetime.datetime.now().strftime('%d%m%Y')}", description="Description of uploaded video.")
    print("Video uploaded to YouTube successfully.")
    
    email_sender = EmailSender()
    email_sender.send_email(recipient_email="cakir_yusuff@outlook.com", subject="About Pipeline", body="Pipeline completed successfully.")
    print("Email sent successfully.")
    
    end = time.time()
    print(f"Process completed successfully. Time taken: {end - start_time} seconds")
    logger.info(f"👌 Pipeline completed successfully. Time taken: {end - start_time} seconds")

    
if __name__ == "__main__":
    main()