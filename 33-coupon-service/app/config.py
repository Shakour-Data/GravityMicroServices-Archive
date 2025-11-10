from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "33-coupon-service"
    PORT: int = 8125
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
