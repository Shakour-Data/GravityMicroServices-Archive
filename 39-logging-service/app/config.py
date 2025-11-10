from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "39-logging-service"
    PORT: int = 8141
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
