from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "29-video-call-service"
    PORT: int = 8121
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
