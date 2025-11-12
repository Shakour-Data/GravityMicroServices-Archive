from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "27-invoice-service"
    PORT: int = 8112
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
