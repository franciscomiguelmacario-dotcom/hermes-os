import os


class HealthCheck:

    def __init__(self, brain):
        self.brain = brain

    def run(self):
        required_paths = [
            "app",
            "app/core",
            "app/core/agents",
            "app/core/tasks",
            "app/core/workflows",
            "app/core/reports",
            "data"
        ]

        missing = [path for path in required_paths if not os.path.exists(path)]

        tasks = self.brain.tasks.all()
        pending = self.brain.tasks.pending()

        return {
            "status": "ok" if not missing else "warning",
            "missing_paths": missing,
            "agents_loaded": list(self.brain.agents.keys()),
            "agents_count": len(self.brain.agents),
            "tasks_total": len(tasks),
            "tasks_pending": len(pending),
            "business_profile": self.brain.business_profile(),
            "obsidian_path": self.brain.reports.get_obsidian_path(),
            "memory_file": "data/memory.json"
        }
