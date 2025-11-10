from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "17-product-service"
    PORT: int = 8102
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
