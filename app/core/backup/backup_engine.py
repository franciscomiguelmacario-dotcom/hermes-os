import json
import os
from datetime import datetime


class BackupEngine:

    def __init__(self, memory):
        self.memory = memory
        self.path = "data/backups"
        os.makedirs(self.path, exist_ok=True)

    def create_backup(self):
        filename = f"hermes_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.path, filename)

        data = self.memory.dump()

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return {
            "status": "backup_created",
            "file": filepath
        }

    def list_backups(self):
        files = sorted(os.listdir(self.path))

        return {
            "status": "ok",
            "backups": files
        }
