from src.news_fetcher import NewsFetcher
from src.text_to_speech import ElevenLabsTTS
from src.did_video import DIDVideoGenerator
from src.gcs_uploader import GCSUploader
from src.youtube_uploader import YouTubeUploader
from src.text_editor import text_editor
import asyncio

from utils import download_video, load_config

def main():
    configs = load_config("config.yaml")
    
    news_fetcher = NewsFetcher()
    news = news_fetcher.fetch_news_content(news_count=2)
    
    # for n in news:
    #     print("**"*20)
    #     print(n)
    # print("**"*20)
    
    edited_news = asyncio.run(text_editor(news))

    # print(f"Edited News: {edited_news}")

    tts_client = ElevenLabsTTS()
    audio_file = tts_client.text_to_speech(
        text=edited_news,
        filename=configs["audio_file"],
    )

    gcs_uploader = GCSUploader(bucket_name=configs["bucket_name"])
    public_url = gcs_uploader.upload_file(audio_file)

    did_client = DIDVideoGenerator()
    video_id = did_client.create_video(audio_url=public_url)
    created_url = did_client.wait_for_video(video_id)

    download_video(created_url, configs["video_file"])

    youtube_uploader = YouTubeUploader(client_secrets_file=configs["client_secret_file"])
    youtube_uploader.authenticate()
    youtube_uploader.upload_video(file_path=configs["video_file"], title="Test video yuklenio", description="Description of uploaded video.")
    
    print("Process completed successfully.")
    
if __name__ == "__main__":
    main()