# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str                   # Full database URL from .env
    SECRET_KEY: str                     # JWT secret key
    ALGORITHM: str                      # JWT algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int    # Token expiry in minutes

    class Config:
        env_file = ".env"               # Reads values from .env automatically
        case_sensitive = False
        
settings = Settings()
