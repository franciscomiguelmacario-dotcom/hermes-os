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
from app.core.autopilot.dropshipping_autopilot import DropshippingAutopilot
from app.core.health.health_check import HealthCheck
from app.core.backup.backup_engine import BackupEngine
from app.core.snapshot.snapshot_engine import SnapshotEngine
from app.core.cycles.business_cycle import BusinessCycle
from app.core.dashboard.dashboard_engine import DashboardEngine

from app.core.connectors.store_connector import StoreConnector
from app.core.connectors.supplier_connector import SupplierConnector
from app.core.integrations.store_api_connector import StoreApiConnector
from app.core.integrations.supplier_api_connector import SupplierApiConnector
from app.core.fulfillment.fulfillment_pipeline import FulfillmentPipeline
from app.core.scoring.product_scoring import ProductScoring
from app.core.pricing.pricing_engine import PricingEngine
from app.core.importer.product_importer import ProductImporter
from app.core.publisher.product_publisher import ProductPublisher
from app.core.pipeline.product_launch_pipeline import ProductLaunchPipeline
from app.core.orders.order_manager import OrderManager
from app.core.orders.order_intake import OrderIntake
from app.core.analytics.sales_analytics import SalesAnalytics
from app.core.campaigns.campaign_manager import CampaignManager
from app.core.notifications.notification_center import NotificationCenter
from app.core.customer_support.support_center import SupportCenter

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
        self.store_api = StoreApiConnector(memory, logger)

        self.supplier = SupplierConnector(memory, logger)
        self.supplier_api = SupplierApiConnector(memory, logger)

        self.scoring = ProductScoring(self.supplier, memory, logger)
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

        self.launch_pipeline = ProductLaunchPipeline(
            self.importer,
            self.publisher,
            self.supplier,
            memory,
            logger,
            self.scoring
        )

        self.order_manager = OrderManager(
            self.store,
            memory,
            logger
        )

        self.sales_analytics = SalesAnalytics(
            self.order_manager,
            memory,
            logger
        )

        self.campaigns = CampaignManager(
            self.store,
            self.sales_analytics,
            memory,
            logger
        )

        self.notifications = NotificationCenter(
            memory,
            logger
        )

        self.order_intake = OrderIntake(
            self.order_manager,
            self.store,
            self.notifications,
            memory,
            logger
        )

        self.customer_support = SupportCenter(
            self.order_manager,
            self.notifications,
            memory,
            logger
        )

        self.fulfillment_pipeline = FulfillmentPipeline(
            self.order_manager,
            self.supplier_api,
            self.notifications,
            memory,
            logger
        )

        self.store_autopilot = DropshippingAutopilot(
            self.launch_pipeline,
            self.campaigns,
            self.order_manager,
            self.sales_analytics,
            memory,
            logger,
            self.notifications,
            self.customer_support,
            self.fulfillment_pipeline
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

    def store_api_config(self):
        return self.store_api.config()

    def set_store_api_config(self, key, value):
        return self.store_api.set_config_value(key, value)

    def push_product_to_store(self, product_id):
        product = self.publisher.get_product(product_id)

        if not product:
            return {
                "status": "error",
                "message": "product not found"
            }

        return self.store_api.push_product(product)

    def sync_products_to_store(self):
        return self.store_api.sync_products(self.store_products())

    def store_api_history(self):
        return self.store_api.history()

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

    def supplier_api_config(self):
        return self.supplier_api.config()

    def set_supplier_api_config(self, key, value):
        return self.supplier_api.set_config_value(key, value)

    def import_order(self, payload, provider="custom"):
        return self.order_intake.import_order(payload, provider)

    def import_test_order(
        self,
        product_id=1,
        customer_name="Cliente Teste",
        customer_email="teste@email.com",
        quantity=1
    ):
        payload = {
            "id": f"TEST-{product_id}",
            "product_id": product_id,
            "quantity": quantity,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "shipping_address": {
                "address1": "Rua Teste 1",
                "city": "Lisboa",
                "country": "Portugal",
                "postal_code": "1000-000"
            }
        }

        return self.order_intake.import_order(payload, "custom")

    def order_intake_history(self):
        return self.order_intake.history()

    def submit_order_to_supplier(self, order_id):
        return self.fulfillment_pipeline.submit_order(order_id)

    def submit_pending_orders_to_supplier(self):
        return self.fulfillment_pipeline.submit_pending_orders()

    def mark_supplier_tracking(self, order_id, tracking_number):
        return self.fulfillment_pipeline.mark_tracking(
            order_id,
            tracking_number
        )

    def fulfillment_pipeline_history(self):
        return self.fulfillment_pipeline.history()

    def supplier_api_history(self):
        return self.supplier_api.history()

    def score_supplier_products(self):
        return self.scoring.score_all()

    def best_supplier_product(self):
        return self.scoring.best_product()

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
        result = self.publisher.publish(product_id)

        config = self.store_api_config()

        if (
            result.get("status") == "product_published"
            and config.get("auto_sync_on_publish")
        ):
            result["store_api_sync"] = self.store_api.push_product(
                result.get("product")
            )

        return result

    def unpublish_product(self, product_id):
        return self.publisher.unpublish(product_id)

    def product_publish_history(self):
        return self.publisher.history()

    def launch_product(self, supplier_product_id, margin_percent=None):
        return self.launch_pipeline.launch_from_supplier_product(
            supplier_product_id,
            margin_percent
        )

    def launch_product_search(self, keyword, margin_percent=None):
        return self.launch_pipeline.launch_first_match(
            keyword,
            margin_percent
        )

    def launch_best_product(self, margin_percent=None):
        return self.launch_pipeline.launch_best_product(margin_percent)

    def product_launch_history(self):
        return self.launch_pipeline.history()

    def orders_all(self):
        return self.order_manager.all()

    def pending_orders(self):
        return self.order_manager.pending()

    def order_detail(self, order_id):
        order = self.order_manager.get_order(order_id)

        if not order:
            return {
                "status": "error",
                "message": "order not found"
            }

        return {
            "status": "ok",
            "order": order
        }

    def create_order(
        self,
        product_id,
        customer_name=None,
        customer_email=None,
        quantity=1
    ):
        result = self.order_manager.create_order(
            product_id,
            customer_name,
            customer_email,
            quantity
        )

        if result.get("status") == "order_created":
            self.notifications.order_confirmation(result.get("order"))

        return result

    def update_order(self, order_id, key, value):
        return self.order_manager.update_order(order_id, key, value)

    def fulfill_order(self, order_id, tracking_number=None):
        result = self.order_manager.fulfill_order(order_id, tracking_number)

        if result.get("status") == "order_fulfilled":
            self.notifications.shipping_confirmation(result.get("order"))

        return result

    def auto_fulfill_orders(self, tracking_prefix="HER"):
        return self.submit_pending_orders_to_supplier()

    def fulfillment_history(self):
        return self.order_manager.fulfillment_history()

    def fulfillment_batches(self):
        return self.order_manager.fulfillment_batches()

    def sales_summary(self):
        return self.sales_analytics.summary()

    def best_selling_products(self):
        return self.sales_analytics.best_selling_products()

    def profit_report(self):
        return self.sales_analytics.profit_report()

    def campaigns_all(self):
        return self.campaigns.all()

    def create_campaign(self, product_id, budget=10, channel="facebook_ads"):
        return self.campaigns.create_campaign(product_id, budget, channel)

    def create_best_campaign(self, budget=10, channel="facebook_ads"):
        return self.campaigns.create_for_best_active_product(budget, channel)

    def launch_campaign(self, campaign_id):
        return self.campaigns.launch_campaign(campaign_id)

    def pause_campaign(self, campaign_id):
        return self.campaigns.pause_campaign(campaign_id)

    def update_campaign_metrics(
        self,
        campaign_id,
        impressions=0,
        clicks=0,
        orders=0,
        revenue=0,
        profit=0,
        spend=0
    ):
        return self.campaigns.update_metrics(
            campaign_id,
            impressions,
            clicks,
            orders,
            revenue,
            profit,
            spend
        )

    def simulate_campaign(self, campaign_id):
        return self.campaigns.simulate_performance(campaign_id)

    def optimize_campaigns(self):
        result = self.campaigns.optimize_campaigns()

        for item in result.get("results", []):
            campaign = self.campaigns.get_campaign(item.get("campaign_id"))

            if campaign:
                self.notifications.campaign_alert(
                    campaign,
                    item.get("action"),
                    item.get("reason")
                )

        return result

    def campaign_performance(self):
        return self.campaigns.performance_report()

    def campaign_report(self):
        return self.campaigns.campaign_report()

    def notifications_all(self):
        return self.notifications.all()

    def pending_notifications(self):
        return self.notifications.pending()

    def send_notifications(self):
        return self.notifications.send_pending()

    def notification_batches(self):
        return self.notifications.batches()

    def support_tickets(self):
        return self.customer_support.all()

    def pending_support_tickets(self):
        return self.customer_support.pending()

    def support_ticket_detail(self, ticket_id):
        ticket = self.customer_support.get_ticket(ticket_id)

        if not ticket:
            return {
                "status": "error",
                "message": "support ticket not found"
            }

        return {
            "status": "ok",
            "ticket": ticket
        }

    def create_support_ticket(
        self,
        customer_email=None,
        subject=None,
        message=None,
        order_id=None
    ):
        return self.customer_support.create_ticket(
            customer_email,
            subject,
            message,
            order_id
        )

    def reply_support_ticket(self, ticket_id, message):
        return self.customer_support.reply_ticket(ticket_id, message)

    def close_support_ticket(self, ticket_id):
        return self.customer_support.close_ticket(ticket_id)

    def auto_reply_support_ticket(self, ticket_id):
        return self.customer_support.auto_reply(ticket_id)

    def auto_reply_support_all(self):
        return self.customer_support.auto_reply_all()

    def support_batches(self):
        return self.customer_support.batches()

    def store_autopilot_config(self):
        return self.store_autopilot.config()

    def set_store_autopilot_config(self, key, value):
        return self.store_autopilot.set_config_value(key, value)

    def store_autopilot_safety(self, requested_budget=0):
        return self.store_autopilot.safety_check(requested_budget)

    def run_store_autopilot(
        self,
        margin_percent=40,
        budget=10,
        channel="facebook_ads",
        tracking_prefix="HER"
    ):
        result = self.store_autopilot.run_cycle(
            margin_percent,
            budget,
            channel,
            tracking_prefix
        )

        config = self.store_api_config()

        if config.get("auto_sync_on_publish"):
            result["store_api_sync"] = self.sync_products_to_store()

        return result

    def store_autopilot_history(self):
        return self.store_autopilot.history()

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
            "store_api_config": self.store_api_config(),
            "supplier_api_config": self.supplier_api_config(),
            "store_products": self.store_products(),
            "supplier_products": self.supplier_products(),
            "orders": self.orders_all(),
            "order_intake_history": self.order_intake_history(),
            "sales_summary": self.sales_summary(),
            "campaigns": self.campaigns_all(),
            "campaign_performance": self.campaign_performance(),
            "store_autopilot_config": self.store_autopilot_config(),
            "notifications": self.notifications_all(),
            "support_tickets": self.support_tickets()
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
