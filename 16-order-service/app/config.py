from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "16-order-service"
    PORT: int = 8101
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
