import json


class LTranslator:
    def __init__(self, path: str) -> None:
        self.ids = {}
        self.path = path

    def add_lang(self, id: int, lang: str) -> None:
        self.ids[id] = lang
    
    def _(self, id: int, key: str = None) -> dict | None:
        with open(f"{self.path}/{self.ids[id]}.json", 'r', encoding='utf-8') as f:
            try:
                d = json.load(f)
                return d if not key else d[key]
            except json.decoder.JSONDecodeError:
                raise f'JSONDecodeError: {self.path}/{self.ids[id]} is empty'