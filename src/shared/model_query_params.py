from typing import overload, Any


class QueryPage:
    default_limit = 1000
    default_offset = 0

    def __init__(self, limit: int or None, offset: int or None) -> None:
        self.limit = limit
        self.offset = offset

    def __call__(self):
        offset = self.offset if self.offset >= 0 else self.default_offset
        limit = self.limit if self.limit > 0 else self.default_limit

        return f"LIMIT {limit} OFFSET {offset}"


class QueryFilter:
    @overload
    def __init__(self, type: str, raw: str) -> None:
        ...

    @overload
    def __init__(self, type: str, field: str, operand: str, value: Any) -> None:
        ...

    def __init__(self, type: str, field_or_raw: str, operand=None, value=None) -> None:
        self.type = type
        self.field_or_raw = field_or_raw
        self.operand = operand
        self.value = value

    def __call__(self):
        if self.operand is None and self.value is None:
            return f"{self.type} {self.field_or_raw}"

        return f"{self.type} {self.field_or_raw} {self.operand} {self.value}"


class QuerySort:
    def __init__(self, field: str, direction="ASC") -> None:
        self.field = field
        self.direction = direction

    def __call__(self):
        return f"{self.field} {self.direction}"


class QueryJoin:
    def __init__(
        self,
        table: str,
        reference: str,
        foreign_key_table: str,
        primary_key_reference: str,
        type="JOIN",
    ) -> None:
        self.table = table
        self.ref = reference
        self.fk = foreign_key_table
        self.pk = primary_key_reference
        self.type = type

    # a simplified join
    def __call__(self):
        return f"""
        {self.type} {self.ref} ON {self.table}.{self.fk} = {self.ref}.{self.pk}
        """


class ModelQueryParams:
    def __init__(
        self,
        joins: list[QueryJoin],
        filters: list[QueryFilter],
        sorts: list[QuerySort],
        page: QueryPage,
    ) -> None:
        self.joins = joins
        self.filters = filters
        self.sorts = sorts
        self.page = page()

    def get_joins(self):
        return "\n".join(list(map(lambda x: x(), self.joins)))

    def get_filters(self):
        return "\n".join(list(map(lambda x: x(), self.filters)))

    def get_sorts(self):
        return ", ".join(list(map(lambda x: x(), self.sorts)))

    def get_page(self):
        return self.page
