from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    EMAIL_USER: str
    EMAIL_PASS: str
    EMAIL_HOST: str
    EMAIL_PORT: int
    PASSWORD_RESET_SECRET: str

    class Config:
        env_file = ".env"  
        env_file_encoding = "utf-8"

settings = Settings() #Creates an instance of the Settings class.
