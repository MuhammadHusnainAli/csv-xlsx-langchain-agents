import os
from pydantic_settings import BaseSettings
from functools import lru_cache

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Settings(BaseSettings):

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    AZURE_OPENAI_API_KEY: str 
    AZURE_OPENAI_ENDPOINT: str 
    AZURE_OPENAI_CHAT_API_VERSION:str
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME_4O: str 
    TEMPERATURE: float = 0.0
    MAX_TOKENS: int = 4096
    DEBUG: bool = True
    
    ALLOWED_EXTENSIONS: set = {".csv", ".xlsx"}
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    
    MAX_QUERY_LIMIT: int = 50
    LLM_DISPLAY_LIMIT: int = 10



@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

