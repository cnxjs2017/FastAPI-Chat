from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/huifa"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
