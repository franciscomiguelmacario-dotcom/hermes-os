from app.core.backup.backup_engine import BackupEngine
from app.core.agents.base_agent import BaseAgent
from app.core.agents.agent_loader import AgentLoader
from app.core.plugins.plugin_loader import PluginLoader
from app.core.runtime.agent_scheduler import AgentScheduler
from app.core.learning_memory import LearningMemory
from app.core.tasks.task_queue import TaskQueue
from app.core.workflows.workflow_engine import WorkflowEngine
from app.core.reports.report_engine import ReportEngine
from app.core.business.business_profile import BusinessProfile
from app.core.decision.decision_engine import DecisionEngine
from app.core.autopilot.autopilot_engine import AutopilotEngine
from app.core.health.health_check import HealthCheck


class Brain:

    def __init__(self, logger=None, memory=None, bus=None):
        self.logger = logger
        self.memory = memory
        self.bus = bus
        self.agents = {}

        self.scheduler = AgentScheduler(logger)
        self.learning = LearningMemory(memory)
        self.tasks = TaskQueue(memory)
        self.workflows = WorkflowEngine(self.tasks, logger)
        self.reports = ReportEngine(memory, self.tasks)
        self.business = BusinessProfile(memory)
        self.decisions = DecisionEngine(memory, self.tasks)
        self.autopilot = AutopilotEngine(
            self.decisions,
            self.tasks,
            self.workflows,
            logger
        )

        self.agent_loader = AgentLoader(logger)
        auto_agents = self.agent_loader.load(self, memory, bus)

        for name, agent in auto_agents.items():
            self.register_agent(name, agent, persist=False)

        self.load_persisted_agents()

        self.plugins = PluginLoader(logger)
        self.plugins.load(self, bus, memory)

        self.health = HealthCheck(self)

        self.backup = BackupEngine(memory)

        self.logger.info("Brain loaded")

    def initialize(self):
        self.logger.info("Brain initialized")

    def register_agent(self, name, agent, persist=True):
        agent.brain = self
        self.agents[name] = agent
        self.logger.info(f"Agent registered: {name}")

        if persist:
            saved = self.memory.get("agents", {})
            saved[name] = {"priority": getattr(agent, "priority", 1)}
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

    def clear_tasks(self):
        return self.tasks.clear()

    def run_workflow(self, name):
        return self.workflows.run(name)

    def report(self):
        return self.reports.business_report()

    def export_report(self):
        return self.reports.export_business_report()

    def export_markdown_report(self):
        return self.reports.export_markdown_report()

    def export_obsidian_report(self):
        return self.reports.export_obsidian_report()

    def set_obsidian_path(self, path):
        return self.reports.set_obsidian_path(path)

    def business_profile(self):
        return self.business.get()

    def set_business_value(self, key, value):
        return self.business.set_value(key, value)

    def next_action(self):
        return self.decisions.next_action()

    def autopilot_once(self):
        return self.autopilot.run_once()

    def autopilot_cycle(self, max_steps=5):
        return self.autopilot.run_cycle(max_steps)

    def health_check(self):
        return self.health.run()

    def create_backup(self):
        return self.backup.create_backup()

    def list_backups(self):
        return self.backup.list_backups()

    def tick(self):
        self.scheduler.run(self.agents)

    def process(self, input_data):
        self.memory.set("last_input", input_data)

        if self.bus:
            self.bus.emit("input.received", input_data)

        self.learning.record("brain", input_data, "processed")

        return f"processed: {input_data}"
