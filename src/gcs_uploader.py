from google.cloud import storage
import os
from dotenv import load_dotenv
import datetime
from src.logger import get_logger

logger = get_logger(__name__)

class GCSUploader:
    def __init__(self, bucket_name):
        load_dotenv()
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_file(self, local_file_path, destination_name=None):
        try:
            logger.info(f"Uploading {local_file_path} to GCS")
            if not destination_name:
                timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                destination_name = f"output{timestamp}.mp3"
            
            blob = self.bucket.blob(destination_name)
            blob.upload_from_filename(local_file_path)
            
            print(f"File {local_file_path} uploaded to {destination_name}.")
            
            url = "https://storage.googleapis.com/{}/{}".format(self.bucket.name, blob.name)
            
            print(f"Public URL: {url}")
            logger.info(f"File uploaded to {url}")
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            raise e
        return url

if __name__ == "__main__":
    uploader = GCSUploader(bucket_name="ai-audio-bucket")
    blob = uploader.upload_file("artifacts/output.mp3")