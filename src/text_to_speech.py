from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import os
from src.logger import get_logger

logger = get_logger(__name__)

class ElevenLabsTTS:
    def __init__(self, api_key: str = None):
        load_dotenv()
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            logger.error("ELEVENLABS_API_KEY environment variable is not set.")
            raise ValueError("API key is required for ElevenLabsTTS")

        self.client = ElevenLabs(api_key=self.api_key)

    def text_to_speech(
        self,
        text: str,
        voice_id: str = "lxZLq5dcyw12UangGJgN",
        model_id: str = "eleven_multilingual_v2",
        output_format: str = "mp3_44100_128",
        filename: str = "output.mp3"
    ):
        try:
            logger.info("Converting text to speech...")
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id=model_id,
                output_format=output_format,
            )
            save(audio, filename=filename)
            logger.info(f"Audio saved to {filename}")
        except Exception as e:
            logger.error(f"Error during text-to-speech conversion: {e}")
            raise e
        return filename


if __name__ == "__main__":
    tts = ElevenLabsTTS()
    output_file = tts.text_to_speech(
        text="Merhaba Ali Erdem Kandemir! aslan parçası.",
        filename="artifacts/output.mp3"
    )
    print(f"Ses dosyası kaydedildi: {output_file}")