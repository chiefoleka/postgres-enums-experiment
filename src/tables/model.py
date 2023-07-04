from shared.model import Model
from shared.demographics import Demographics
from typing import Any


class Profile(Model):
    _has_join = []

    def __init__(self):
        super().__init__()
        self.table = "profiles"
        self.demographics = Demographics()

    def should_column_have_a_table(self, column, value):
        if column in self.demographics.get_names_only():
            return True

        return False

    def select(self, *columns):
        formatted = []
        for column in columns:
            if self.should_column_have_a_table(column):
                self.inner_join(column, f"{column}_id")
                self._has_join.append(column)
                formatted.append(f"{column}.name AS {column}")

        return super().select(*formatted)

    def _where(self, type: str, field: str, operand: str, value: Any):
        formatted_field = field
        if self.should_column_have_a_table(field):
            if field not in self._has_join:
                self.inner_join(field, f"{field}_id")
                self._has_join.append(field)
            formatted_field = f"{field}.name"

        return super()._where(type, formatted_field, operand, value)
