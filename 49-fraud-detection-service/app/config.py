from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "49-fraud-detection-service"
    PORT: int = 8151
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
