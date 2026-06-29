class BaseAgent:

    def __init__(self, name, memory, logger, bus, brain=None, priority=1):
        self.name = name
        self.memory = memory
        self.logger = logger
        self.bus = bus
        self.brain = brain
        self.priority = priority

    def tick(self):
        pass

    def act(self, data):
        self.logger.info(f"[{self.name}] {data}")
