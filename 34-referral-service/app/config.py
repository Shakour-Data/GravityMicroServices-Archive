from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "34-referral-service"
    PORT: int = 8126
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
