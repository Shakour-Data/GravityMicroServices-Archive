from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "41-webhook-service"
    PORT: int = 8143
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
