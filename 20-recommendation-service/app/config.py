from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "20-recommendation-service"
    PORT: int = 8105
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
