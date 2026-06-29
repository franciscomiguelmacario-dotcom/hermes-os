import json
from pathlib import Path


class Memory:

    def __init__(self, file="data/memory.json"):
        self.file = Path(file)
        self.file.parent.mkdir(parents=True, exist_ok=True)

        if not self.file.exists():
            self.file.write_text("{}", encoding="utf-8")

        self.load()

    def load(self):
        self.data = json.loads(self.file.read_text(encoding="utf-8"))

    def save(self):
        self.file.write_text(
            json.dumps(self.data, indent=4),
            encoding="utf-8"
        )

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def delete(self, key):
        self.data.pop(key, None)
        self.save()

    def all(self):
        return self.data
