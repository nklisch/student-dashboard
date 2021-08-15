from pydantic import BaseSettings


class Settings(BaseSettings):
    PRODUCTION: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
