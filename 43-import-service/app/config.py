from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "43-import-service"
    PORT: int = 8145
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
