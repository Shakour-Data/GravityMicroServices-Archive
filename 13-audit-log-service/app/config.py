from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "13-audit-log-service"
    PORT: int = 8089
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
