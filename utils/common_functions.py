import urllib.request
from src.logger import get_logger

logger = get_logger(__name__)

def download_video(url: str, save_path: str) -> None:
    """
    Verilen URL'den videoyu indirir ve belirtilen yola kaydeder.

    Args:
        url (str): İndirilecek video URL'si.
        save_path (str): Videonun kaydedileceği dosya yolu.
    """
    try:
        logger.info("Video downloading started.")
        urllib.request.urlretrieve(url, save_path)
        print(f"Video başarıyla indirildi ve {save_path} konumuna kaydedildi.")
        logger.info("Video successfully downloaded.")
        return True
    except Exception as e:
        print(f"Video indirme sırasında bir hata oluştu: {e}")
        logger.error(f"Error downloading video: {e}")
        raise e

def load_config(file_path: str) -> dict:
    import yaml
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Configuration loaded from {file_path}")
            return config
    except Exception as e:
        logger.error(f"Error loading configuration from {file_path}: {e}")
        raise e
    