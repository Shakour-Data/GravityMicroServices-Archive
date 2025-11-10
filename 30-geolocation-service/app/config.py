from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "30-geolocation-service"
    PORT: int = 8122
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
