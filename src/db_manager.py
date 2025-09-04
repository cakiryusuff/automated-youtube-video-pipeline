import psycopg2
from utils.common_functions import load_config
from logger import get_logger
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Tuple
from psycopg2.extras import RealDictCursor

@dataclass
class CreditRecord:
    service: str
    used: int
    remaining: int
    total: int
    timestamp: datetime

class DatabaseManager:
    def __init__(self):
        self.logger = get_logger(__name__)
        configs = load_config("config/config.yaml")
        db_config = configs.get("database", {})
        self.host = db_config.get("host", "localhost")
        self.database = db_config.get("dbname", "youtube_api_db")
        self.user = db_config.get("user", "postgres")
        self.password = db_config.get("password", "yourpassword")
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.logger.info("Database connection established.")
            self._init_db()
        except Exception as e:
            self.logger.error(f"Error connecting to database: {e}")
            raise
        
    def _init_db(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS credit_usage (
            id SERIAL PRIMARY KEY,
            service VARCHAR(50) NOT NULL,
            used INTEGER NOT NULL,
            remaining INTEGER NOT NULL,
            total INTEGER NOT NULL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_credit_usage_service ON credit_usage(service);
        CREATE INDEX IF NOT EXISTS idx_credit_usage_timestamp ON credit_usage(recorded_at);
        """
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(create_table_query)
            self.connection.commit()
            self.logger.info("Database initialized successfully.")
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
            self.connection.rollback()
            raise
    
    def insert_credit_usage(self, service: str, used: int, remaining: int, total: int):
        try:
            query = """
            INSERT INTO credit_usage (service, used, remaining, total)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """
            
            with self.connection.cursor() as cursor:
                cursor.execute(query, (service, used, remaining, total))
                record_id = cursor.fetchone()[0]
                self.connection.commit()
            
            self.logger.info(f"Inserted credit usage record with ID: {record_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error inserting credit usage: {e}")
            self.connection.rollback()
            return False
    
    def get_latest_credits(self, service: str) -> Optional[CreditRecord]:
        """ Returns the latest credit record for the given service """
        try:
            query = """
            SELECT service, used, remaining, total, recorded_at
            FROM credit_usage
            WHERE service = %s
            ORDER BY recorded_at DESC
            LIMIT 1
            """
            
            with self.connection.cursor() as cursor:
                cursor.execute(query, (service,))
                result = cursor.fetchone()
                
                if result:
                    return CreditRecord(
                        service=result[0],
                        used=result[1],
                        remaining=result[2],
                        total=result[3],
                        timestamp=result[4]
                    )
                    
                return None
        except Exception as e:
            self.logger.error(f"Error fetching latest credits: {e}")
            return None
        
    def get_credit_history(self, service: str, days: int = 7) -> list:
        """ Returns credit records for the given service in the last 'days' days """
        try:
            query = """
            SELECT service, used, remaining, total, recorded_at
            FROM credit_usage
            WHERE service = %s AND recorded_at >= NOW() - INTERVAL '%s days'
            ORDER BY recorded_at DESC
            """
            
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (service, days))
                results = cursor.fetchall()
                
                return [
                    CreditRecord(
                        service=row[0],
                        used=row[1],
                        remaining=row[2],
                        total=row[3],
                        timestamp=row[4]
                    ) for row in results
                ]
                
        except Exception as e:
            self.logger.error(f"Error fetching credit history: {e}")
            return []
    
    def close(self):
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed.")
            
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.connect()
    db_manager.insert_credit_usage("ElevenLabs", 100, 900, 1000)
    latest = db_manager.get_latest_credits("ElevenLabs")
    print(latest)
    history = db_manager.get_credit_history("ElevenLabs", days=30)
    for record in history:
        print(record)
    db_manager.close()