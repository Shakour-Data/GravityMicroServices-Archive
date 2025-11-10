from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "46-ab-testing-service"
    PORT: int = 8148
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
