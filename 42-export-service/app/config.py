from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "42-export-service"
    PORT: int = 8144
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
