from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "40-scheduler-service"
    PORT: int = 8142
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
