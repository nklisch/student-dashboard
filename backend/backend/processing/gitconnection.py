from pydantic import BaseSettings, PostgresDsn, validator
from pydantic import BaseSettings
from github import Github


class Settings(BaseSettings):
    GITHUB_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

github = Github(settings.GITHUB_KEY)
