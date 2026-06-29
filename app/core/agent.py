class Agent:

    def __init__(self, name, memory=None, logger=None, bus=None, goal_manager=None, learner=None):
        self.name = name
        self.memory = memory
        self.logger = logger
        self.bus = bus
        self.goal_manager = goal_manager
        self.learner = learner

    def act(self, data):

        if self.logger:
            self.logger.info(f"[{self.name}] action: {data}")

        if self.learner:
            self.learner.record(self.name, self.memory.get("last_input"), data)
