from app.core.agents.base_agent import BaseAgent


class AnalyzerAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=1):
        super().__init__(name, memory, logger, bus, brain, priority)

        if self.bus:
            self.bus.subscribe("input.received", self.on_input)

    def on_input(self, data):
        self.logger.info(f"[analyzer] received: {data}")

        patterns = self.memory.get("input_patterns", {})
        patterns[data] = patterns.get(data, 0) + 1
        self.memory.set("input_patterns", patterns)

        if patterns[data] >= 2:
            self.logger.info(f"[analyzer] repeated input detected: {data}")

        if "spawn" in data and self.brain:
            from app.core.agents.base_agent import BaseAgent

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
