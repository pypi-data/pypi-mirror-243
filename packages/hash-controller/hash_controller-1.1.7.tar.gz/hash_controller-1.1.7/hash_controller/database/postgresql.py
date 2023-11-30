import time
import psycopg2
from hash_controller.database.database_interface import DataBase
from hash_controller.database.db_credentials import DataBaseCredentials
from hash_controller.settings import Settings


settings = Settings()


class PostgreSQL(DataBase):
    def __init__(self, cre: DataBaseCredentials) -> None:
        self.conn = psycopg2.connect(
            host=cre.db_host,
            database=settings.HASH_DB_NAME,
            user=cre.db_user,
            password=cre.db_pass,
            port=cre.db_port,
        )
        self._session = self.conn.cursor()
        self.DB_PK1 = "customer"
        self.DB_PK2 = "entity"
        self.DB_PK3 = "hash"

    def find_one(self, customer_uuid, type, id):
        sql = f"SELECT * FROM {settings.HASH_DB_TABLE} WHERE {self.DB_PK1}='{customer_uuid}' AND {self.DB_PK2}='{type}' AND {self.DB_PK3}='{id}';"
        self._session.execute(sql)
        return self._session.fetchone()

    def find(self, customer_uuid, type, ids_to_find: list):
        sql = f"SELECT * FROM {settings.HASH_DB_TABLE} WHERE {self.DB_PK1}='{customer_uuid}' AND {self.DB_PK2}='{type}' AND {self.DB_PK3} IN {tuple(ids_to_find)};"
        self._session.execute(sql)
        items = self._session.fetchall()
        return [item[2] for item in items]

    def insert_one(self, customer_uuid, type, id):
        sql = f"INSERT INTO {settings.HASH_DB_TABLE}({self.DB_PK1}, {self.DB_PK2}, {self.DB_PK3}, created_at) VALUES(%s, %s, %s, %s);"
        response = self._session.execute(sql, (customer_uuid, type, id, int(time.time())))
        self.conn.commit()
        return response

    def insert_many(self, customer_uuid, type, ids):
        now = int(time.time())
        sql = f"INSERT INTO {settings.HASH_DB_TABLE}({self.DB_PK1}, {self.DB_PK2}, {self.DB_PK3}, created_at) VALUES(%s, %s, %s, %s);"
        response = self._session.executemany(sql, [(customer_uuid, type, id, now) for id in ids])
        self.conn.commit()
        return response
