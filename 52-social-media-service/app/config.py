from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "52-social-media-service"
    PORT: int = 8154
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
