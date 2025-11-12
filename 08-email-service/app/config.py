from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "08-email-service"
    PORT: int = 8086
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
