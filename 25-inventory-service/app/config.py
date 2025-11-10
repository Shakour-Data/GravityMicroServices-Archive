from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "25-inventory-service"
    PORT: int = 8110
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
