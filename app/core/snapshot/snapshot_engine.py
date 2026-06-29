import json
import os
from datetime import datetime


class SnapshotEngine:

    def __init__(self, brain):
        self.brain = brain
        self.path = "data/snapshots"
        os.makedirs(self.path, exist_ok=True)

    def create_snapshot(self):
        snapshot = {
            "created_at": datetime.now().isoformat(),
            "health": self.brain.health_check(),
            "business_profile": self.brain.business_profile(),
            "next_action": self.brain.next_action(),
            "tasks": self.brain.tasks.all(),
            "report": self.brain.report(),
            "memory": self.brain.memory.dump()
        }

        filename = f"hermes_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.path, filename)

        with open(filepath, "w") as f:
            json.dump(snapshot, f, indent=4, ensure_ascii=False)

        return {
            "status": "snapshot_created",
            "file": filepath
        }

    def list_snapshots(self):
        return {
            "status": "ok",
            "snapshots": sorted(os.listdir(self.path))
        }

    def restore_snapshot(self, filename):
        safe_name = os.path.basename(filename)
        filepath = os.path.join(self.path, safe_name)

        if not os.path.exists(filepath):
            return {
                "status": "error",
                "message": f"snapshot not found: {safe_name}"
            }

        with open(filepath, "r") as f:
            snapshot = json.load(f)

        memory = snapshot.get("memory")

        if not isinstance(memory, dict):
            return {
                "status": "error",
                "message": "invalid snapshot memory"
            }

        self.brain.memory.data = memory
        self.brain.memory._save()

        return {
            "status": "snapshot_restored",
            "file": filepath
        }
