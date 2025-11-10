from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "19-search-service"
    PORT: int = 8104
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
