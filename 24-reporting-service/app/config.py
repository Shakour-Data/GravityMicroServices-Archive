from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "24-reporting-service"
    PORT: int = 8109
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
