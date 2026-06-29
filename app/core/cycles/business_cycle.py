import time


class BusinessCycle:

    def __init__(self, brain, logger):
        self.brain = brain
        self.logger = logger

    def run_dropshipping_cycle(self, wait_seconds=8):
        before = self.brain.create_snapshot()

        workflow = self.brain.run_workflow("dropshipping")

        time.sleep(wait_seconds)

        report = self.brain.report()
        obsidian = self.brain.export_obsidian_report()
        after = self.brain.create_snapshot()

        return {
            "status": "business_cycle_finished",
            "workflow": workflow,
            "report": report,
            "obsidian": obsidian,
            "snapshot_before": before,
            "snapshot_after": after
        }
