class Kernel:

    def __init__(self, brain, logger):
        self.brain = brain
        self.logger = logger

    def boot(self):
        self.logger.info("Kernel booting...")
        self.brain.initialize()

        try:
            snapshot = self.brain.create_snapshot()
            self.logger.info(f"Startup snapshot created: {snapshot['file']}")
        except Exception as error:
            self.logger.info(f"Startup snapshot failed: {error}")

        self.logger.info("Kernel ready")

    def run_tick(self):
        self.brain.tick()
