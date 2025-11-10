from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "47-feature-flag-service"
    PORT: int = 8149
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
