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
