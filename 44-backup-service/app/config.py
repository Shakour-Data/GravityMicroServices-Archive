from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "44-backup-service"
    PORT: int = 8146
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
