from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "28-chat-service"
    PORT: int = 8120
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
