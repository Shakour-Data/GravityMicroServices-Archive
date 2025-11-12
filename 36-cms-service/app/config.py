from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "36-cms-service"
    PORT: int = 8128
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
