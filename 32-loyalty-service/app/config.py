from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "32-loyalty-service"
    PORT: int = 8124
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
