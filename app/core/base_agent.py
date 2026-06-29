class BaseAgent:

    def __init__(self, name, memory, logger, bus, brain=None):
        self.name = name
        self.memory = memory
        self.logger = logger
        self.bus = bus
        self.brain = brain
