from app.core.agents.analyzer import AnalyzerAgent
from app.core.agents.executor import ExecutorAgent
from app.core.agents.product_research import ProductResearchAgent
from app.core.agents.marketing import MarketingAgent
from app.core.agents.organic import OrganicTrafficAgent
from app.core.agents.base_agent import BaseAgent
from app.core.plugins.plugin_loader import PluginLoader
from app.core.runtime.agent_scheduler import AgentScheduler
from app.core.learning_memory import LearningMemory
from app.core.tasks.task_queue import TaskQueue


class Brain:

    def __init__(self, logger=None, memory=None, bus=None):
        self.logger = logger
        self.memory = memory
        self.bus = bus
        self.agents = {}

        self.scheduler = AgentScheduler(logger)
        self.learning = LearningMemory(memory)
        self.tasks = TaskQueue(memory)

        self.register_agent(
            "analyzer",
            AnalyzerAgent("analyzer", memory, logger, bus, self, priority=10),
            persist=False
        )

        self.register_agent(
            "product_research",
            ProductResearchAgent("product_research", memory, logger, bus, self, priority=8),
            persist=False
        )

        self.register_agent(
            "marketing",
            MarketingAgent("marketing", memory, logger, bus, self, priority=7),
            persist=False
        )

        self.register_agent(
            "organic",
            OrganicTrafficAgent("organic", memory, logger, bus, self, priority=6),
            persist=False
        )

        self.register_agent(
            "executor",
            ExecutorAgent("executor", memory, logger, bus, self, priority=5),
            persist=False
        )

        self.load_persisted_agents()

        self.plugins = PluginLoader(logger)
        self.plugins.load(self, bus, memory)

        self.logger.info("Brain loaded")

    def initialize(self):
        self.logger.info("Brain initialized")

    def register_agent(self, name, agent, persist=True):
        agent.brain = self
        self.agents[name] = agent
        self.logger.info(f"Agent registered: {name}")

        core_agents = ["analyzer", "executor", "product_research", "marketing", "organic"]

        if persist and name not in core_agents:
            saved = self.memory.get("agents", {})
            saved[name] = {
                "priority": getattr(agent, "priority", 1)
            }
            self.memory.set("agents", saved)

    def load_persisted_agents(self):
        saved = self.memory.get("agents", {})

        if isinstance(saved, list):
            saved = {name: {"priority": 1} for name in saved}

        for name, meta in saved.items():
            if name not in self.agents:
                agent = BaseAgent(
                    name,
                    self.memory,
                    self.logger,
                    self.bus,
                    self,
                    priority=meta.get("priority", 1)
                )
                self.agents[name] = agent
                self.logger.info(f"Persisted agent loaded: {name}")

    def set_priority(self, name, priority):
        if name not in self.agents:
            return False

        self.agents[name].priority = int(priority)

        saved = self.memory.get("agents", {})
        if name in saved:
            saved[name]["priority"] = int(priority)
            self.memory.set("agents", saved)

        return True

    def create_task(self, title):
        task = self.tasks.add(title)

        if self.bus:
            self.bus.emit("task.created", task)

        return task

    def tick(self):
        self.scheduler.run(self.agents)

    def process(self, input_data):
        self.memory.set("last_input", input_data)

        if self.bus:
            self.bus.emit("input.received", input_data)

        self.learning.record("brain", input_data, "processed")

        return f"processed: {input_data}"
