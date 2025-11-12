from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "14-cache-service"
    PORT: int = 8091
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
