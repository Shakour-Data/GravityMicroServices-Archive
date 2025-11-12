from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "18-cart-service"
    PORT: int = 8103
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
