import requests
import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from src.logger import get_logger
from src.db_manager import DatabaseManager

load_dotenv()

class CreditTracker:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.did_api_key = os.getenv("DID_API_KEY")
        self.did_url = "https://api.d-id.com/credits"
        self.elevenlabs_url = "https://api.elevenlabs.io/v1/user"
        self.did_url_headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.did_api_key}"
            }
        
        self.db_manager = DatabaseManager()
        
    def get_did_credits(self) -> int:
        try:
            self.logger.info("Fetching D-ID credits...")
            response = requests.get(self.did_url, headers=self.did_url_headers)
            response.raise_for_status()
            data = response.json()
            credits = data.get("remaining", 0)
            self.logger.info(f"D-ID available credits: {credits}")
            return credits
        except requests.RequestException as e:
            self.logger.error(f"Error fetching D-ID credits: {e}")
            raise e
        
    def get_elevenlabs_credits(self):
        try:
            self.logger.info("Fetching ElevenLabs character usage...")
            client = ElevenLabs(api_key=self.elevenlabs_api_key)
            user_data = client.user.get()
            used_character_count = user_data.subscription.character_count
            character_limit = user_data.subscription.character_limit
            remaining_characters = int(character_limit) - int(used_character_count)
            self.logger.info(f"ElevenLabs used characters: {used_character_count}, remaining characters: {remaining_characters}")
            return used_character_count, remaining_characters, character_limit
        except requests.exceptions.RequestException as e:
            print(f"API hatası: {e}")
            return None
        
    def save_to_db(self):
        did_credits = self.get_did_credits()
        elevenlabs_credits = self.get_elevenlabs_credits()
        self.db_manager.insert_credit_usage("ElevenLabs", elevenlabs_credits[0], elevenlabs_credits[1], elevenlabs_credits[2])
        self.db_manager.insert_credit_usage("D-ID", did_credits, did_credits, did_credits)
        
if __name__ == "__main__":
    credit_tracker = CreditTracker()
    credit_tracker.save_to_db()