from app.core.agents.analyzer import AnalyzerAgent
from app.core.plugins.plugin_loader import PluginLoader


class Brain:

    def __init__(self, logger=None, memory=None, bus=None):
        self.logger = logger
        self.memory = memory
        self.bus = bus
        self.agents = {}

        self.register_agent(
            "analyzer",
            AnalyzerAgent("analyzer", memory, logger, bus, self)
        )

        self.plugins = PluginLoader(logger)
        self.plugins.load(self, bus, memory)

        self.logger.info("Brain loaded")

    def initialize(self):
        self.logger.info("Brain initialized")

    def register_agent(self, name, agent):
        self.agents[name] = agent
        self.logger.info(f"Agent registered: {name}")

    def tick(self):
        for agent in self.agents.values():
            if hasattr(agent, "tick"):
                agent.tick()

    def process(self, input_data):
        self.memory.set("last_input", input_data)

        if self.bus:
            self.bus.emit("input.received", input_data)

        return f"processed: {input_data}"
