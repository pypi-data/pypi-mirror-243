import json
import os
import time
from unittest.mock import patch
import uuid
import pymongo
import mongomock

os.environ["HASH_DB_TYPE"] = "mongodb"
os.environ["APP_ENV"] = "develop"
os.environ["HASH_DB_TABLE"] = "hash_table"

with mongomock.patch(servers=(("localhost", 27017),),):
    with patch("hash_controller.aws_manager.get_secret") as secret:
        secret.return_value = json.dumps({"db_host": "localhost", "db_user": "user", "db_pass": "mongo", "db_port": 27017})
        client = pymongo.MongoClient("localhost")["hash_table"]
        from hash_controller.main import HashClient


    def test_exist_false():
        customer_uuid = uuid.UUID("c85dc072-7d2e-4f1c-9b8a-b872d0c0be24")
        type = "user"
        hash = HashClient._get_hash({"user": "222"})
        client[f"{customer_uuid}#{type}"].insert_one({"_id": hash})
        response = HashClient.exist(customer_uuid, type, {"user": "123"})
        client[f"{customer_uuid}#{type}"].delete_many({})
        assert response == False


    def test_exist_true():
        customer_uuid = "c85dc072-7d2e-4f1c-9b8a-b872d0c0be24"
        type = "user"
        hash = HashClient._get_hash({"user": "123"})
        client[f"{customer_uuid}#{type}"].insert_one({"_id": hash, "created_at": int(time.time())})
        response = HashClient.exist(customer_uuid, type, {"user": "123"})
        client[f"{customer_uuid}#{type}"].delete_many({})
        assert response == True


    def test_exist_many():
        customer_uuid = uuid.UUID("c85dc072-7d2e-4f1c-9b8a-b872d0c0be24")
        type = "user"
        hash_1 = HashClient._get_hash({"user": "123"})
        hash_2 = HashClient._get_hash({"user": "456"})
        hash_3 = HashClient._get_hash({"user": "789"})
        client[f"{customer_uuid}#{type}"].insert_many([{"_id": hash_1}, {"_id": hash_2}, {"_id": hash_3}])
        response = HashClient.exist_many(customer_uuid, type, [{"user": "123"}, {"user": "456"}, {"user": "222"}])
        client[f"{customer_uuid}#{type}"].delete_many({})
        assert isinstance(response, list)
        assert response[0] == True
        assert response[1] == True
        assert response[2] == False


    def test_create():
        customer_uuid = "c85dc072-7d2e-4f1c-9b8a-b872d0c0be24"
        type = "user"
        hash = HashClient._get_hash({"user": "123"})
        response = HashClient.create(customer_uuid, type, {"user": "123"})
        item = client[f"{customer_uuid}#{type}"].find_one(hash)
        client[f"{customer_uuid}#{type}"].delete_many({})
        assert response == hash
        assert item


    def test_create_many():
        customer_uuid = uuid.UUID("c85dc072-7d2e-4f1c-9b8a-b872d0c0be24")
        type = "user"
        hash_1 = HashClient._get_hash({"user": "123"})
        hash_2 = HashClient._get_hash({"user": "456"})
        hash_3 = HashClient._get_hash({"user": "789"})
        response = HashClient.create_many(customer_uuid, type, [{"user": "123"}, {"user": "456"}, {"user": "789"}])
        item_1 = client[f"{customer_uuid}#{type}"].find_one(hash_1)
        item_2 = client[f"{customer_uuid}#{type}"].find_one(hash_2)
        item_3 = client[f"{customer_uuid}#{type}"].find_one(hash_3)
        client[f"{customer_uuid}#{type}"].delete_many({})
        assert response == [hash_1, hash_2, hash_3]
        assert item_1
        assert item_2
        assert item_3


    def test_check_customer_uuid_empty():
        customer_uuid = ""
        type = "user"
        obj = {"user": 123}
        response = HashClient.exist(customer_uuid, type, obj)
        assert response == False


    def test_check_customer_uuid_none():
        customer_uuid = None
        type = "user"
        obj = {"user": 123}
        response = HashClient.exist(customer_uuid, type, obj)
        assert response == False


    def test_check_type_empty():
        customer_uuid = "123"
        type = ""
        obj = {"user": 123}
        response = HashClient.exist(customer_uuid, type, obj)
        assert response == False


    def test_check_type_none():
        customer_uuid = "123"
        type = None
        obj = {"user": 123}
        response = HashClient.exist(customer_uuid, type, obj)
        assert response == False


    def test_check_obj_none():
        customer_uuid = "123"
        type = "user"
        obj = None
        response = HashClient.exist(customer_uuid, type, obj)
        assert response == False


    def test_check_obj_empty():
        customer_uuid = "123"
        type = "user"
        obj = {}
        response = HashClient.exist(customer_uuid, type, obj)
        assert response == False


    def test_check_objs_none():
        customer_uuid = "123"
        type = "user"
        objs = None
        response = HashClient.exist_many(customer_uuid, type, objs)
        assert response == False


    def test_check_objs_not_list():
        customer_uuid = "123"
        type = "user"
        objs = {"user": 1}
        response = HashClient.exist_many(customer_uuid, type, objs)
        assert response == False


    def test_check_objs_empty():
        customer_uuid = "123"
        type = "user"
        objs = []
        response = HashClient.exist_many(customer_uuid, type, objs)
        assert response == []


    def test_check_objs_with_empty_item():
        customer_uuid = "123"
        type = "user"
        objs = [{}]
        response = HashClient.exist_many(customer_uuid, type, objs)
        assert response == [False]
