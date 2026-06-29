from app.core.auto_repair import AutoRepair


class SafeExecutor:

    def __init__(self, logger):
        self.logger = logger
        self.repair = AutoRepair(logger)

    def run(self, fn, fallback=None):

        try:
            return fn()

        except Exception as e:

            action = self.repair.fix(e)
            self.logger.error(f"auto-repair action: {action}")

            return fallback
