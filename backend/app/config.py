from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    App Configuration & Secret Environment Variables
    """
    APP_NAME: str = "CodeSentinel AI"
    ENVIRONMENT: str = "dev"
    
    # Security Configuration
    # (In production, replace with a long random secret string)
    SECRET_KEY: str = "super_secret_codesentinel_key_change_in_production_12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # Tokens expire in 1 hour
    
    # AI Config
    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()