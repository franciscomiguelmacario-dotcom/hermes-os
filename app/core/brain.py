from app.core.router import Router
from app.core.logger import Logger


class Brain:

    def __init__(self):

        self.logger = Logger()

        self.router = Router()

        self.router.register("status", self.status)
        self.router.register("hello", self.hello)

    def status(self):

        self.logger.success("Hermes operacional.")

    def hello(self):

        self.logger.info("Olá, eu sou o Hermes.")

    def execute(self, command):

        self.router.execute(command)
