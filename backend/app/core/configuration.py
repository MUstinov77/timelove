from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    AUTH_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ISSUER: str
    TOKEN_EXPIRE_HOURS: int
    TITLE: str = "Timelove"
    DB_USER: str
    DB_PASSWORD: str
    ATTACHMENTS_DIRECTORY_PATH: str = f"{Path(__file__).parents[2]}/attachments/"
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    TEST_DB_STAT: bool = False

    @property
    def DB_URI(self): # noqa
        ## try load driver via config file
        # try:
        #     import DB_DRIVER
        # except ImportError:
        #     import asyncpg

        ## add driver param to db_uri path
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def REDIS_URI(self): # noqa
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[2].joinpath(".env")
    )


def get_settings() -> Settings:
    return Settings()


settings = Settings()
