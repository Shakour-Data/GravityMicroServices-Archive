from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "10-file-storage-service"
    PORT: int = 8088
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
