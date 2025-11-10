from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "04-config-service"
    PORT: int = 8090
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
