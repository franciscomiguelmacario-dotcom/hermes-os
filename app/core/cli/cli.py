class CLI:

    def __init__(self, brain, logger):
        self.brain = brain
        self.logger = logger

    def run(self):

        self.logger.info("CLI started")

        while True:
            cmd = input("> ").strip()

            if cmd == "exit":
                break

            if cmd == "status":
                self.logger.info({
                    "agents": list(self.brain.agents.keys())
                })
                continue

            if cmd.startswith("run "):
                data = cmd[4:]
                result = self.brain.process(data)
                self.logger.info(result)
                continue

            self.logger.info("unknown command")
