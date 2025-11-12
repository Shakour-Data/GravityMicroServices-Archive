from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "09-sms-service"
    PORT: int = 8087
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
