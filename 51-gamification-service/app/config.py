from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "51-gamification-service"
    PORT: int = 8153
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
