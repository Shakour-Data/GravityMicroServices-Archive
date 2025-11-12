from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "26-shipping-service"
    PORT: int = 8111
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
