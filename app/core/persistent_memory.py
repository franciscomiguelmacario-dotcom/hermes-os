import json
import os


class PersistentMemory:

    def __init__(self, path="data/memory.json"):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f)

    def set(self, key, value):
        self.data[key] = value
        self._save()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def dump(self):
        return self.data
