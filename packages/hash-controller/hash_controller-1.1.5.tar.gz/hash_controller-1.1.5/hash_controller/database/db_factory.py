from enum import Enum
import json
from hash_controller.aws_manager import get_secret
from hash_controller.database.database_interface import DataBase
from hash_controller.database.db_credentials import DataBaseCredentials
from hash_controller.database.dynamodb import DynamoDB
from hash_controller.database.mongodb import MongoDB
from hash_controller.database.postgresql import PostgreSQL
from hash_controller.settings import Settings


settings = Settings()


class DataBaseTypes(Enum):
    MONGODB = "mongodb"
    POSTGRESQL = "postgresql"
    DYNAMODB = "dynamodb"


class DataBaseFactory:
    def __init__(self) -> None:
        try:
            self._database_type = DataBaseTypes(settings.HASH_DB_TYPE)
        except:
            return None

    def get_database(self) -> DataBase:
        try:
            mapper = {
                DataBaseTypes.MONGODB: MongoDB,
                DataBaseTypes.POSTGRESQL: PostgreSQL,
                DataBaseTypes.DYNAMODB: DynamoDB,
            }
            credentials = self._get_credentials()
            return mapper[self._database_type](credentials)
        except:
            return None

    def _get_credentials(self) -> DataBaseCredentials:
        if self._database_type is DataBaseTypes.DYNAMODB:
            return DataBaseCredentials()
        if self._database_type is DataBaseTypes.MONGODB:
            secret_credentials = f"PLATFORM-CREDENTIAL-MONGODB-{settings.APP_ENV.upper()}"
        if self._database_type is DataBaseTypes.POSTGRESQL:
            secret_credentials = f"PLATFORM-CREDENTIAL-DB-{settings.APP_ENV.upper()}"
        connection_string_database = json.loads(get_secret(key=secret_credentials))
        credentials = DataBaseCredentials(**connection_string_database)
        if settings.APP_ENV == "localhost":
            from sshtunnel import SSHTunnelForwarder

            ssh_tunnel = SSHTunnelForwarder(
                credentials.db_host,
                ssh_username=settings.SSH_USER,
                ssh_private_key=settings.SSH_KEY_PATH,
                remote_bind_address=(settings.SSH_LOCAL_HOST, settings.SSH_LOCAL_PORT),
            )

            ssh_tunnel.start()
            credentials.db_host = settings.SSH_LOCAL_HOST
            credentials.db_port = str(ssh_tunnel.local_bind_port)

        return credentials
