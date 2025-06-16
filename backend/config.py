from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = f"{os.getenv('DATABASE_URL')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = os.getenv('LOG_FILE')