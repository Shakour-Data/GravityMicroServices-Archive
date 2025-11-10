from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "11-permission-service"
    PORT: int = 8083
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
