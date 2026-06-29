class AgentScheduler:

    def __init__(self, logger=None):
        self.logger = logger

    def run(self, agents):
        ordered = sorted(
            agents.items(),
            key=lambda item: getattr(item[1], "priority", 1),
            reverse=True
        )

        for name, agent in ordered:
            if hasattr(agent, "tick"):
                agent.tick()
