from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Setup directories
BACKEND_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BACKEND_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    # Match the exact names from your .env file
    PROJECT_NAME: str = "Resume AI Platform"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/resume_ai"
    REDIS_URL: str = "redis://localhost:6379"
    
    JWT_SECRET: str = "dev-secret-key"
    JWT_ALGORITHM: str = "HS256"
    
    # Pydantic will automatically convert the string "60" from your .env into an int
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Pydantic v2 configuration management
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Protects your app from crashing if extra variables exist in the environment
    )


settings = Settings()