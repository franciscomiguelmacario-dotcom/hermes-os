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

        with open(filepath, "w") as f:
            json.dump(self.memory.dump(), f, indent=4, ensure_ascii=False)

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

    def restore_backup(self, filename):
        safe_name = os.path.basename(filename)
        filepath = os.path.join(self.path, safe_name)

        if not os.path.exists(filepath):
            return {
                "status": "error",
                "message": f"backup not found: {safe_name}"
            }

        with open(filepath, "r") as f:
            data = json.load(f)

        self.memory.data = data
        self.memory._save()

        return {
            "status": "backup_restored",
            "file": filepath
        }
