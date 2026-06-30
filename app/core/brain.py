
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
from app.core.backup.backup_engine import BackupEngine
from app.core.snapshot.snapshot_engine import SnapshotEngine
from app.core.cycles.business_cycle import BusinessCycle
from app.core.dashboard.dashboard_engine import DashboardEngine

from app.core.connectors.store_connector import StoreConnector
from app.core.connectors.supplier_connector import SupplierConnector
from app.core.pricing.pricing_engine import PricingEngine
from app.core.importer.product_importer import ProductImporter
from app.core.publisher.product_publisher import ProductPublisher

from app.core.command_center.command_center import CommandCenter
from app.core.llm.ollama_client import OllamaClient
from app.core.voice.speech_engine import SpeechEngine
from app.core.voice.listen_engine import ListenEngine
from app.core.voice.jarvis_mode import JarvisMode


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

        self.store = StoreConnector(memory, logger)
        self.supplier = SupplierConnector(memory, logger)
        self.pricing = PricingEngine(memory, logger)

        self.importer = ProductImporter(
            self.store,
            self.supplier,
            self.pricing,
            memory,
            logger
        )

        self.publisher = ProductPublisher(
            self.store,
            memory,
            logger
        )

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
        self.snapshot = SnapshotEngine(self)
        self.business_cycle = BusinessCycle(self, logger)
        self.dashboard = DashboardEngine(self)

        self.command_center = CommandCenter(self, logger)
        self.llm = OllamaClient()
        self.speech = SpeechEngine(memory, logger)
        self.listener = ListenEngine(memory, logger)
        self.jarvis_mode = JarvisMode(self, logger)

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

    def store_config(self):
        return self.store.config()

    def set_store_value(self, key, value):
        return self.store.set_value(key, value)

    def store_products(self):
        return self.store.products()

    def create_store_product(self, title, price=None, cost=None):
        return self.store.create_product(title, price, cost)

    def update_store_product(self, product_id, key, value):
        return self.store.update_product(product_id, key, value)

    def delete_store_product(self, product_id):
        return self.store.delete_product(product_id)

    def supplier_config(self):
        return self.supplier.config()

    def set_supplier_value(self, key, value):
        return self.supplier.set_value(key, value)

    def supplier_products(self):
        return self.supplier.products()

    def add_supplier_product(
        self,
        title,
        cost=None,
        shipping_days=None,
        supplier_url=None,
        category=None
    ):
        return self.supplier.add_product(
            title,
            cost,
            shipping_days,
            supplier_url,
            category
        )

    def search_supplier_products(self, keyword):
        return self.supplier.search(keyword)

    def delete_supplier_product(self, product_id):
        return self.supplier.delete_product(product_id)

    def pricing_config(self):
        return self.pricing.config()

    def set_pricing_value(self, key, value):
        return self.pricing.set_value(key, value)

    def calculate_price(self, cost, shipping=0, margin_percent=None):
        return self.pricing.calculate(cost, shipping, margin_percent)

    def import_supplier_product(self, supplier_product_id, margin_percent=None):
        return self.importer.import_supplier_product(
            supplier_product_id,
            margin_percent
        )

    def import_supplier_search(self, keyword, margin_percent=None):
        return self.importer.import_first_match(
            keyword,
            margin_percent
        )

    def product_import_history(self):
        return self.importer.history()

    def product_detail(self, product_id):
        product = self.publisher.get_product(product_id)

        if not product:
            return {
                "status": "error",
                "message": "product not found"
            }

        return {
            "status": "ok",
            "product": product
        }

    def publish_product(self, product_id):
        return self.publisher.publish(product_id)

    def unpublish_product(self, product_id):
        return self.publisher.unpublish(product_id)

    def product_publish_history(self):
        return self.publisher.history()

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

    def restore_backup(self, filename):
        return self.backup.restore_backup(filename)

    def create_snapshot(self):
        return self.snapshot.create_snapshot()

    def list_snapshots(self):
        return self.snapshot.list_snapshots()

    def restore_snapshot(self, filename):
        return self.snapshot.restore_snapshot(filename)

    def run_business_cycle(self, wait_seconds=8):
        return self.business_cycle.run_dropshipping_cycle(wait_seconds)

    def business_cycle_history(self):
        return self.business_cycle.history()

    def dashboard_data(self):
        return self.dashboard.data()

    def handle_command(self, text):
        return self.command_center.handle(text)

    def chat(self, text):
        context = {
            "business_profile": self.business_profile(),
            "next_action": self.next_action(),
            "tasks": self.tasks.all(),
            "store_config": self.store_config(),
            "store_products": self.store_products(),
            "supplier_products": self.supplier_products()
        }

        prompt = f"""
Tu és o Hermes, um sistema de automação para dropshipping.

Contexto atual:
{context}

Pedido do utilizador:
{text}

Responde em português, de forma curta, prática e direta.
"""

        return self.llm.generate(prompt)

    def speak(self, text):
        return self.speech.speak(text)

    def handle_command_voice(self, text):
        result = self.handle_command(text)
        self.speak(result)
        return result

    def voice_config(self):
        return self.speech.config()

    def set_voice_value(self, key, value):
        return self.speech.set_value(key, value)

    def listen_config(self):
        return self.listener.config()

    def set_listen_value(self, key, value):
        return self.listener.set_value(key, value)

    def listen_once(self, seconds=None):
        return self.listener.listen_once(seconds)

    def listen_and_handle(self, seconds=None):
        heard = self.listen_once(seconds)

        if heard.get("status") != "ok":
            return heard

        text = heard.get("text", "")
        result = self.handle_command_voice(text)

        return {
            "status": "handled_voice_command",
            "heard": text,
            "result": result
        }

    def start_jarvis_mode(self, cycles=10, seconds=5):
        return self.jarvis_mode.start(cycles, seconds)

    def tick(self):
        self.scheduler.run(self.agents)

    def process(self, input_data):
        self.memory.set("last_input", input_data)

        if self.bus:
            self.bus.emit("input.received", input_data)

        self.learning.record("brain", input_data, "processed")

        return f"processed: {input_data}"
