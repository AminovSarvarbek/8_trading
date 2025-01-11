import json


class LTranslator:
    def __init__(self, path: str) -> None:
        self.ids = {}
        self.path = path

    def add_lang(self, id: int, lang: str) -> None:
        self.ids[id] = lang
    
    def _(self, id: int, key: str = None) -> dict | None:
        with open(f"{self.path}/{self.ids[id]}.json") as f:
            try:
                d = json.load(f)
                return d if not key else d[key]
            except json.decoder.JSONDecodeError:
                raise f'JSONDecodeError: {self.path}/{self.ids[id]} is empty'

lt = LTranslator(path='locales')

lt.add_lang(id=1, lang="uz")
messages = lt._(id=1)
print(messages)

