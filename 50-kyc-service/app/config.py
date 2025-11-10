from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "50-kyc-service"
    PORT: int = 8152
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
