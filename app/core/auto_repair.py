class AutoRepair:

    def __init__(self, logger):
        self.logger = logger

    def fix(self, error):

        msg = str(error)

        if "IndentationError" in msg:
            self.logger.error("Detected indentation issue")
            return "check_indentation"

        if "KeyError" in msg:
            self.logger.error("Missing key detected")
            return "check_agents_or_memory"

        if "ImportError" in msg:
            self.logger.error("Missing module detected")
            return "check_imports"

        return "unknown_error"
