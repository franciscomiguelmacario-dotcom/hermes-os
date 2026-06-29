class ExecutorAgent:

    def __init__(self, logger):
        self.logger = logger

    def act(self, data):
        self.logger.info(f"[executor] executing: {data}")
