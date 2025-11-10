from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "21-review-service"
    PORT: int = 8106
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
