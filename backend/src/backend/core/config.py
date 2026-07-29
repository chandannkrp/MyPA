from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    ENV:str = "development"
    LOG_LEVEL:str = "INFO"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8"
)
    
settings = Settings()