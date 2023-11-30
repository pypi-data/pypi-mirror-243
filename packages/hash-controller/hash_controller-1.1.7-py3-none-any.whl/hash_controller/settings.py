import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Database
    HASH_DB_NAME: str = os.getenv("HASH_DB_NAME")
    HASH_DB_TABLE: str = os.getenv("HASH_DB_TABLE")
    HASH_DB_TYPE: str = os.getenv("HASH_DB_TYPE")
    APP_ENV: str = os.getenv("APP_ENV")

    # SSH
    SSH_USER: str = os.getenv("SSH_USER")
    SSH_KEY_PATH: str = os.getenv("SSH_KEY_PATH")
    SSH_LOCAL_HOST: str = os.getenv("SSH_LOCAL_HOST")
    SSH_LOCAL_PORT: int = os.getenv("SSH_LOCAL_PORT")

    # AWS
    AWS_REGION: str = os.getenv("AWS_REGION")
    AWS_CREDENTIAL_KEY: str = os.getenv("AWS_CREDENTIAL_KEY_PLATFORM")
    AWS_CREDENTIAL_SECRET: str = os.getenv("AWS_CREDENTIAL_SECRET_PLATFORM")
