import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Question-Answering Bot API"
    PROJECT_VERSION: str = "1.0.0"
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "qa_bot_db")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY")
    ALLOWED_ORIGINS: list = ["*"]  # Modify this in production

    class Config:
        env_file = ".env"

settings = Settings()