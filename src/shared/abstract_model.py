from abc import ABC
from shared.database import Database
from psycopg2.extras import DictRow
from shared.model_query_params import ModelQueryParams


class AbstractModel(ABC):
    def __init__(self):
        self.db = Database()

    def explain(self, sql) -> DictRow:
        sql = f"EXPLAIN (ANALYZE, FORMAT JSON) {sql}"

        return self.db.query(sql)

    def find_by_id(
        self, id: int, table_name: str, columns: tuple = ("*"), explain=False
    ) -> DictRow:
        sql = f"""
            SELECT {','.join(columns)}
            FROM {table_name}
            WHERE id = {id}
        """

        if explain:
            return self.explain(sql)

        return self.db.select_one(sql)

    def find_by(
        self,
        table_name: str,
        columns: tuple = ("*"),
        params: ModelQueryParams = {},
        explain=False,
    ):
        sorting = (f"ORDER BY {params.get_sorts()}") if params.get_sorts() != "" else ""
        sql = f"""
            SELECT {','.join(columns)}
            FROM {table_name}
            {params.get_joins()}
            WHERE true
            {params.get_filters()}
            {params.get_sorts()}
            {sorting}
        """

        if explain:
            return self.explain(sql)

        return self.db.select_many()
