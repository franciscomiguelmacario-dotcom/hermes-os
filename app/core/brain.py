from app.core.agents.analyzer import AnalyzerAgent
from app.core.agents.base_agent import BaseAgent
from app.core.plugins.plugin_loader import PluginLoader


class Brain:

    def __init__(self, logger=None, memory=None, bus=None):
        self.logger = logger
        self.memory = memory
        self.bus = bus
        self.agents = {}

        self.register_agent(
            "analyzer",
            AnalyzerAgent("analyzer", memory, logger, bus, self),
            persist=False
        )

        self.load_persisted_agents()

        self.plugins = PluginLoader(logger)
        self.plugins.load(self, bus, memory)

        self.logger.info("Brain loaded")

    def initialize(self):
        self.logger.info("Brain initialized")

    def register_agent(self, name, agent, persist=True):
        self.agents[name] = agent
        self.logger.info(f"Agent registered: {name}")

        if persist and name != "analyzer":
            agents = self.memory.get("agents", [])
            if name not in agents:
                agents.append(name)
                self.memory.set("agents", agents)

    def load_persisted_agents(self):
        saved_agents = self.memory.get("agents", [])

        for name in saved_agents:
            if name not in self.agents:
                agent = BaseAgent(name, self.memory, self.logger, self.bus, self)
                self.agents[name] = agent
                self.logger.info(f"Persisted agent loaded: {name}")

    def tick(self):
        for agent in self.agents.values():
            if hasattr(agent, "tick"):
                agent.tick()

    def process(self, input_data):
        self.memory.set("last_input", input_data)

        if self.bus:
            self.bus.emit("input.received", input_data)

        return f"processed: {input_data}"
