import time
from pymongo import MongoClient
from hash_controller.database.database_interface import DataBase
from hash_controller.database.db_credentials import DataBaseCredentials
from hash_controller.settings import Settings


settings = Settings()


class MongoDB(DataBase):
    def __init__(self, cre: DataBaseCredentials) -> None:
        self._client = MongoClient(f"mongodb://{cre.db_user}:{cre.db_pass}@{cre.db_host}:{cre.db_port}/")
        self._session = self._client[settings.HASH_DB_TABLE]
        self.id = "_id"

    def find_one(self, customer_uuid, type, id):
        return self._session[f"{customer_uuid}#{type}"].find_one(id)

    def find(self, customer_uuid, type, ids_to_find):
        items = self._session[f"{customer_uuid}#{type}"].find(
            filter={self.id: {"$in": ids_to_find}}, projection=self.id
        )
        return [item[self.id] for item in items]

    def insert_one(self, customer_uuid, type, id):
        obj = {self.id: id, "created_at": int(time.time())}
        return self._session[f"{customer_uuid}#{type}"].insert_one(obj).inserted_id

    def insert_many(self, customer_uuid, type, ids):
        now = int(time.time())
        objs = [{self.id: id, "created_at": now} for id in ids]
        return self._session[f"{customer_uuid}#{type}"].insert_many(objs).inserted_ids
