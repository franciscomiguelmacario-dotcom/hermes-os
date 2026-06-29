from app.core.agents.base_agent import BaseAgent


class AnalyzerAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=1):
        super().__init__(name, memory, logger, bus, brain, priority)

        self.bus.subscribe("input.received", self.on_input)

    def on_input(self, data):
        self.logger.info(f"[analyzer] received: {data}")

        if "spawn" in data and self.brain:
            agent = BaseAgent(
                "dynamic_agent",
                self.memory,
                self.logger,
                self.bus,
                self.brain
            )

            self.brain.register_agent("dynamic_agent", agent)
            self.logger.info("dynamic_agent created")

    def tick(self):
        pass
