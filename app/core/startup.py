from app.core.logger import Logger
from app.core.memory import PersistentMemory
from app.core.bus.event_bus import EventBus
from app.core.brain import Brain
from app.core.kernel.kernel import Kernel
from app.core.runtime.runtime import Runtime
from app.core.cli.cli import CLI


class Hermes:

    def __init__(self):

        self.logger = Logger()
        self.memory = PersistentMemory()
        self.bus = EventBus()

        self.brain = Brain(self.logger, self.memory, self.bus)
        self.kernel = Kernel(self.brain, self.logger)

        self.cli = CLI(self.brain, self.logger)
        self.runtime = Runtime(self.kernel, self.logger, self.cli)

    def start(self):
        self.runtime.start()


if __name__ == "__main__":
    Hermes().start()
