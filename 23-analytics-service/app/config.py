from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "23-analytics-service"
    PORT: int = 8108
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
