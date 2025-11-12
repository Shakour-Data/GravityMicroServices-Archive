from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "22-wishlist-service"
    PORT: int = 8107
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
