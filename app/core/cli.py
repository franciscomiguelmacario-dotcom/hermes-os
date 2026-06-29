class CLI:

    def __init__(self, cc, logger):
        self.cc = cc
        self.logger = logger

    def run(self):

        self.logger.info("CLI ready")

        while True:
            cmd = input("> ")

            if cmd == "exit":
                break

            result = self.cc.execute(cmd)

            if result is not None:
                self.logger.info(result)
