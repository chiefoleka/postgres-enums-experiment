from shared.abstract_model import AbstractModel
from shared.model_query_params import (
    ModelQueryParams,
    QueryJoin,
    QueryFilter,
    QuerySort,
    QueryPage,
)
from typing import overload, Any, TypeVar
from psycopg2.extras import DictRow

Self = TypeVar("Self", bound="Model")


class Model(AbstractModel):
    table = ""
    columns: tuple = "*"
    joins: list[QueryJoin] = []
    wheres: list[QueryFilter] = []
    sorts: list[QuerySort] = []
    limit: int = None
    offset: int = None

    def select(self, *columns) -> Self:
        self.columns = columns

        return self

    def _join(
        self, reference: str, foreign_key: str, primary_key: str, type: str
    ) -> Self:
        join = QueryJoin(
            table=self.table,
            reference=reference,
            foreign_key_table=foreign_key,
            primary_key_reference=primary_key,
            type=type,
        )

        self.joins.append(join)

        return self

    def join(self, reference: str, foreign_key: str, primary_key="id") -> Self:
        return self._join(reference, foreign_key, primary_key, "JOIN")

    def left_join(self, reference: str, foreign_key: str, primary_key="id") -> Self:
        return self._join(reference, foreign_key, primary_key, "LEFT JOIN")

    def inner_join(self, reference: str, foreign_key: str, primary_key="id") -> Self:
        return self._join(reference, foreign_key, primary_key, "INNER JOIN")

    def _where(self, type: str, field: str, operand: str, value: Any) -> Self:
        where = QueryFilter(type=type, field=field, operand=operand, value=value)

        self.wheres.append(where)

        return self

    @overload
    def and_where(self, field: str, value: str) -> Self:
        ...

    @overload
    def and_where(self, field: str, operand: str, value: Any) -> Self:
        ...

    def and_where(self, field: str, value_or_operand: str, value: Any) -> Self:
        value = value_or_operand if value is None else value
        operand = value_or_operand if value is not None else "="

        return self._where("AND", field, operand, value)

    @overload
    def or_where(self, field: str, value: str) -> Self:
        ...

    @overload
    def or_where(self, field: str, operand: str, value: Any) -> Self:
        ...

    def or_where(self, field: str, value_or_operand: str, value: Any) -> Self:
        value = value_or_operand if value is None else value
        operand = value_or_operand if value is not None else "="

        return self._where("OR", field, operand, value)

    def where_raw(self, type: str, raw: str) -> Self:
        where = QueryFilter(type=type, raw=raw)

        self.wheres.append(where)

        return self

    def _order_by(self, field: str, direction: str) -> Self:
        order = QuerySort(field=field, direction=direction)

        self.sorts.append(order)

        return self

    def order_by_desc(self, field) -> Self:
        return self._order_by(field, "DESC")

    def order_by_asc(self, field) -> Self:
        return self._order_by(field, "ASC")

    def take(self, limit, offset=None) -> Self:
        self.limit = limit
        self.offset = offset

        return self

    def _get_query_params(self) -> ModelQueryParams:
        page = QueryPage(self.limit, self.offset)
        params = ModelQueryParams(
            joins=self.joins, filters=self.wheres, sorts=self.sorts, page=page
        )

        return params

    def get(self) -> list[DictRow]:
        params = self._get_query_params()

        return self.find_by(table_name=self.table, columns=self.columns, params=params)

    def explain(self) -> ModelQueryParams:
        params = self._get_query_params()

        return self.find_by(
            table_name=self.table, columns=self.columns, params=params, explain=True
        )

    def get_and_explain(self) -> dict:
        return {"results": self.get(), "explain": self.explain()}
