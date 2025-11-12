from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "37-feedback-service"
    PORT: int = 8129
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
