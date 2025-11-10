from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "48-tax-service"
    PORT: int = 8150
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
