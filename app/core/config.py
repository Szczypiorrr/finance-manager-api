from dotenv import load_dotenv
import os

load_dotenv()

def get_db_url():
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        db_url = "sqlite:///./finance.db"

    return db_url