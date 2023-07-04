from shared.model import Model
from shared.demographics import Demographics
from typing import Any


class Profile(Model):
    def __init__(self):
        super().__init__()
        self.table = "profiles"
        self.demographics = Demographics()

    def get_column_enum_translation(self, column, value):
        if column in self.demographics.get_names_only():
            return self.demographics.get_value_translation(column, value)

        return value

    def get_column_translation_label(self, column, value):
        if column in self.demographics.get_names_only():
            return self.demographics.get_translation_label(column, value)

        return value

    def _where(self, type: str, field: str, operand: str, value: Any):
        translated_value = self.get_column_enum_translation(field, value)

        return super()._where(type, field, operand, translated_value)

    def get(self):
        results = super().get()

        for result in results:
            for key, value in result:
                result[key] = self.get_column_translation_label(value)

        return result
