from app.core.logger import Logger
from app.core.config import Config
from app.core.database import Database
from app.core.events import EventBus
from app.core.scheduler import Scheduler
from app.plugins.registry import PluginRegistry
from app.core.memory import Memory
from app.core.brain import Brain


class Hermes:

    def __init__(self):

        self.logger = Logger()
        self.config = Config()
        self.database = Database()
        self.events = EventBus()
        self.scheduler = Scheduler()
        self.memory = Memory()
        self.plugins = PluginManager()
        self.brain = Brain()

    def start(self):

        self.logger.info("A iniciar Hermes...")

        self.database.initialize()

        self.scheduler.start()

        self.plugins.load()
        self.plugins.start()

        self.logger.success("Hermes iniciado")
