class Kernel:

    def __init__(self, brain, logger):
        self.brain = brain
        self.logger = logger

    def boot(self):
        self.logger.info("Kernel booting...")
        self.brain.initialize()
        self.logger.info("Kernel ready")

    def run_tick(self):
        self.brain.tick()
