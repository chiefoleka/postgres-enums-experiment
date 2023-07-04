import json


class Demographics:
    def __init__(self) -> None:
        self.original_data = json.load(open("./data/demographics.json", "r"))
        self.data = self.prepare(self.original_data)

    def _format_v_key(self, value):
        # normalize the names, so Non-binary becomes NON_BINARY
        return value.upper().replace("-", "_").replace(" ", "_")

    def prepare(self, data) -> dict:
        file_content = {}
        for key, values in data.items():
            formatted_values = {}

            numerial = 1
            for value in values:
                formatted_values[self._format_v_key(value)] = numerial
                numerial += 1

            file_content[key] = formatted_values

        return file_content

    def get_names_only(self) -> list:
        return list(self.original_data.keys())

    def get_values(self, name) -> list:
        return self.original_data[name] if name in self.original_data else []

    def get_value_translation(self, name, option):
        values = self.data[name] if name in self.data else {}

        v_key = self._format_v_key(option)

        return values[v_key] if v_key in values else None

    def get_translation_label(self, name, translated_value):
        # get the translation values
        values = list(self.data[name].values) if name in self.data else []

        v_index = values.index(translated_value)

        return self.original_data[name][v_index]

    def __call__(self, name=None, option=None) -> dict:
        if name is not None:
            values = self.data[name] if name in self.data else {}

            if option is not None:
                v_key = self._format_v_key(option)
                return values[v_key] if v_key in values else ""

            return values
        return self.data
