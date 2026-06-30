import time
from datetime import datetime


class BusinessCycle:

    def __init__(self, brain, logger):
        self.brain = brain
        self.logger = logger

    def run_dropshipping_cycle(self, wait_seconds=8):
        cycle_started = datetime.now().isoformat()

        before = self.brain.create_snapshot()
        workflow = self.brain.run_workflow("dropshipping")

        time.sleep(wait_seconds)

        report = self.brain.report()
        obsidian = self.brain.export_obsidian_report()
        after = self.brain.create_snapshot()

        result = {
            "status": "business_cycle_finished",
            "started_at": cycle_started,
            "finished_at": datetime.now().isoformat(),
            "workflow": workflow,
            "report": report,
            "obsidian": obsidian,
            "snapshot_before": before,
            "snapshot_after": after
        }

        history = self.brain.memory.get("business_cycles", [])
        history.append({
            "started_at": result["started_at"],
            "finished_at": result["finished_at"],
            "status": result["status"],
            "tasks_total": report.get("tasks_total"),
            "tasks_done": report.get("tasks_done"),
            "tasks_pending": report.get("tasks_pending"),
            "obsidian_file": obsidian.get("file")
        })

        self.brain.memory.set("business_cycles", history)

        return result

    def history(self):
        return self.brain.memory.get("business_cycles", [])
