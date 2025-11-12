from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "12-session-service"
    PORT: int = 8084
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
