from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "45-rate-limiter-service"
    PORT: int = 8147
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
