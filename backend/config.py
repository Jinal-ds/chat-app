from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "chat_app"
    JWT_SECRET: str = "supersecretkey-changethis-inproduction"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 60

    class Config:
        env_file = ".env"          # reads from .env file if present
        extra = "allow"            # allows extra env vars from Docker

settings = Settings()