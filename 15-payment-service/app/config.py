from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "15-payment-service"
    PORT: int = 8100
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
