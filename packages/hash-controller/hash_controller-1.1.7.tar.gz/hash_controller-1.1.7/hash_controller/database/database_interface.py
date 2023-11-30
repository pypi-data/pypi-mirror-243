import abc


class DataBase(abc.ABC):
    @abc.abstractmethod
    def find_one(self, customer_uuid, type, id):
        pass

    @abc.abstractmethod
    def find(self, customer_uuid, type, ids_to_find):
        pass

    @abc.abstractmethod
    def insert_one(self, customer_uuid, type, id):
        pass

    @abc.abstractmethod
    def insert_many(self, customer_uuid, type, ids):
        pass
