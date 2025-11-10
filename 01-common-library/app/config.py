from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "01-common-library"
    PORT: int = N/A
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
