from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "35-translation-service"
    PORT: int = 8127
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
