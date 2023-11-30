import hashlib
import json
import logging

from hash_controller.database.db_factory import DataBaseFactory


class HashClient:
    _database = DataBaseFactory().get_database()

    @staticmethod
    def exist(customer_uuid: str, type: str, obj) -> bool:
        """Check if an item is hashed in the database

        Args:
            customer_uuid (str): customer_uuid
            type (str): type of the obj to be stored
            obj (Any): object to be checked

        Raises:
            ValueError: parameters not valid

        Returns:
            bool: True if the item exist, False if don't
        """
        try:
            HashClient._check_customer_and_type(customer_uuid, type)
            HashClient._check_obj(obj)
            id = HashClient._get_hash(obj)
            item = HashClient._database.find_one(customer_uuid, type, id)
            if item is None:
                return False
            else:
                return True
        except Exception as err:
            logging.error(f"[Hash Controller]{err.args}")
            return False

    @staticmethod
    def exist_many(customer_uuid: str, type: str, objs: list) -> list[bool]:
        """Check if many item are hashed in the database

        Args:
            customer_uuid (str): customer_uuid
            type (str): type of the obj to be stored
            objs (list): list of objects to be checked

        Raises:
            TypeError: objs is not a list
            ValueError: parameters not valid

        Returns:
            list[bool]: True if the item exist, False if it doesn't
        """
        try:
            HashClient._check_objs(objs)
            HashClient._check_customer_and_type(customer_uuid, type)
            ids_to_find = []
            for obj in objs:
                HashClient._check_obj(obj)
                id = HashClient._get_hash(obj)
                ids_to_find.append(id)

            items = HashClient._database.find(customer_uuid, type, ids_to_find)
            results = []
            for id_to_find in ids_to_find:
                if id_to_find in items:
                    results.append(True)
                else:
                    results.append(False)
            return results
        except Exception as err:
            logging.error(f"[Hash Controller]{err.args}")
            if isinstance(objs, list):
                return [False for _ in objs]
            return False

    @staticmethod
    def create(customer_uuid: str, type: str, obj) -> str:
        """Create a hashed item in the database

        Args:
            customer_uuid (str): customer_uuid
            type (str): type of the obj to be stored
            obj (Any): object to be checked

        Raises:
            TypeError: obj is None
            ValueError: customer_uuid or type empty strings
            DuplicateKeyError: obj already exist

        Returns:
            str: id stored "{customer_uuid}/{type}/{hash}"
        """
        try:
            HashClient._check_customer_and_type(customer_uuid, type)
            HashClient._check_obj(obj)
            id = HashClient._get_hash(obj)
            return HashClient._database.insert_one(customer_uuid, type, id)
        except Exception as err:
            logging.error(f"[Hash Controller]{err.args}")
            return False

    @staticmethod
    def create_many(customer_uuid: str, type: str, objs: list) -> list[str]:
        """Create many hashed item in the database

        Args:
            customer_uuid (str): customer_uuid
            type (str): type of the obj to be stored
            objs (list): list of objects to be checked

        Raises:
            TypeError: objs is not a list
            ValueError: customer_uuid or type empty strings
            BulkWriteError: any of the items already exist

        Returns:
            list[str]: list of ids stored "{customer_uuid}/{type}/{hash}"
        """
        try:
            HashClient._check_objs(objs)
            HashClient._check_customer_and_type(customer_uuid, type)
            ids_to_add = []
            for obj in objs:
                HashClient._check_obj(obj)
                id = HashClient._get_hash(obj)
                ids_to_add.append(id)
            return HashClient._database.insert_many(customer_uuid, type, ids_to_add)
        except Exception as err:
            logging.error(f"[Hash Controller]{err.args}")
            return False

    @staticmethod
    def _check_customer_and_type(customer_uuid, type):
        if not customer_uuid or not str(customer_uuid):
            raise ValueError(f"customer_uuid not valid. Value: {customer_uuid}")
        if not type or not str(type):
            raise ValueError(f"type not valid. Value: {type}")

    @staticmethod
    def _check_obj(obj):
        if not obj:
            raise ValueError(f"Obj not valid. {obj}")

    @staticmethod
    def _check_objs(objs):
        if not isinstance(objs, list):
            raise TypeError(f"Objs of type {objs.__class__} is not valid.")

        if not objs:
            raise ValueError(f"objs is an empty list")

    @staticmethod
    def _get_hash(obj):
        jsonObj = json.dumps(obj)
        hash = hashlib.md5(jsonObj.encode("utf-8")).hexdigest()
        return hash
