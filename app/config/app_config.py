import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "Langquence API")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # 실행 환경 설정
    APP_EXECUTE_COMMAND: str = os.getenv("APP_EXECUTE_COMMAND", "main:app")
    APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT: int = int(os.getenv("APP_PORT", "8080"))
    APP_RELOAD: bool = os.getenv("APP_RELOAD", "True").lower() == "true"
    
    # API 키 설정
    ALIBABA_API_KEY: str = os.getenv("ALIBABA_API_KEY", "")
    
    # 모델 설정
    MODEL_NAME: str = os.getenv("MODEL_NAME", "qwen-max")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "512"))
    
    # 로그 설정
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()