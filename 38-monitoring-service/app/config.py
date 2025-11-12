from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "38-monitoring-service"
    PORT: int = 8140
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
