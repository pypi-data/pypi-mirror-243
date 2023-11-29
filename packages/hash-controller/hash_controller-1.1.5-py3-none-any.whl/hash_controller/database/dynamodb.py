import time
from hash_controller.database.database_interface import DataBase
from hash_controller.database.db_credentials import DataBaseCredentials
from hash_controller.settings import Settings
import boto3

settings = Settings()


class DynamoDB(DataBase):
    def __init__(self, cre: DataBaseCredentials) -> None:
        self._dynamo = boto3.resource(
            "dynamodb",
            aws_access_key_id=settings.AWS_CREDENTIAL_KEY,
            aws_secret_access_key=settings.AWS_CREDENTIAL_SECRET,
            region_name=settings.AWS_REGION,
        )
        self._session = self._dynamo.Table(settings.HASH_DB_TABLE)
        self.DB_FK = "customer-entity"
        self.DB_SK = "hasth"

    def find_one(self, customer_uuid, type, id):
        return self._session.get_item(Key={self.DB_FK: f"{customer_uuid}#{type}", self.DB_SK: id})

    def find(self, customer_uuid, type, ids_to_find):
        batch_keys = [{self.DB_FK: f"{customer_uuid}#{type}", self.DB_SK: id} for id in ids_to_find]
        response = self._session.batch_get_item(RequestItems=batch_keys)
        return response

    def insert_one(self, customer_uuid, type, id):
        self._session.put_item(
            Item={self.DB_FK: f"{customer_uuid}#{type}", self.DB_SK: id, "created_at": int(time.time())}
        )
        return

    def insert_many(self, customer_uuid, type, ids):
        now = int(time.time())
        with self._session.batch_writer() as batch:
            for id in ids:
                batch.put_item(Item={self.DB_FK: f"{customer_uuid}#{type}", self.DB_SK: id, "created_at": now})
        return
