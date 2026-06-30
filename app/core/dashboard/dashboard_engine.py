class DashboardEngine:

    def __init__(self, brain):
        self.brain = brain

    def data(self):
        tasks = self.brain.tasks.all()
        pending = self.brain.tasks.pending()

        return {
            "status": "ok",
            "health": self.brain.health_check(),
            "business_profile": self.brain.business_profile(),
            "next_action": self.brain.next_action(),
            "agents": {
                name: getattr(agent, "priority", 1)
                for name, agent in self.brain.agents.items()
            },
            "tasks": {
                "total": len(tasks),
                "done": len([t for t in tasks if t["status"] == "done"]),
                "pending": len(pending),
                "items": tasks
            },
            "cycle_history": self.brain.business_cycle_history(),
            "report": self.brain.report()
        }
