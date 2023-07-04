import psycopg2
from psycopg2.extensions import cursor as _Cursor
from psycopg2.extensions import connection as _Connection
from psycopg2.extras import DictRow
from psycopg2.extras import RealDictCursor
from decouple import config


class Database:
    def __init__(self):
        self.conn = self._db_conn()

    def _db_conn(self) -> _Connection:
        host = config("POSTGRES_HOST")
        port = config("POSTGRES_PORT")
        database = config("POSTGRES_DB")
        user = config("POSTGRES_USER")
        password = config("POSTGRES_PASSWORD")

        return psycopg2.connect(
            host=host, port=port, database=database, user=user, password=password
        )

    def _exec(self, callback: _Cursor):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        result = callback(cursor)
        self.conn.commit()

        cursor.close()

        return result

    def query(self, sql: str) -> DictRow:
        def handler(cursor: _Cursor):
            cursor.execute(sql)

        return self._exec(handler)

    def select_one(self, sql: str) -> DictRow:
        def handler(cursor: _Cursor):
            cursor.execute(sql)

            return cursor.fetchone()

        return self._exec(handler)

    def select_many(self, sql: str) -> list[DictRow]:
        def handler(cursor: _Cursor):
            cursor.execute(sql)

            return cursor.fetchall()

        return self._exec(handler)

    def insert_one(self, table: str, columns: tuple, data: list) -> DictRow:
        markers = ["%s" for _ in range(len(columns))]
        sql = f"""
            INSERT INTO {table} ({','.join(columns)})
            VALUES ({','.join(markers)})
            RETURNING *
        """

        def handler(cursor: _Cursor):
            cursor.execute(sql, data)

            return cursor.fetchone()

        return self._exec(handler)

    def insert_many(
        self, table: str, columns: tuple, data: list[list]
    ) -> list[DictRow]:
        markers = ",".join(["%s" for _ in range(len(columns))])
        markers_array = ",".join([f"({markers})" for _ in range(len(data))])

        sql = f"""
            INSERT INTO {table} ({','.join(columns)})
            VALUES {markers_array}
            RETURNING *
        """

        bindings = [item for inner in data for item in inner]

        def handler(cursor: _Cursor):
            cursor.execute(sql, bindings)

            return cursor.fetchall()

        return self._exec(handler)

    def insert_batch(self, table: str, columns: tuple, data: list[list]) -> None:
        markers = ["%s" for _ in range(len(columns))]
        sql = f"""
            INSERT INTO {table} ({','.join(columns)})
            VALUES ({','.join(markers)})
        """

        def handler(cursor: _Cursor):
            cursor.executemany(sql, data)

        return self._exec(handler)

    def __del__(self):
        self.conn.close()
