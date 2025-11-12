from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "31-subscription-service"
    PORT: int = 8123
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
