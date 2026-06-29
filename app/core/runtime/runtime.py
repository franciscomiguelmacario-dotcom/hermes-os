import threading
import time


class Runtime:

    def __init__(self, kernel, logger, cli):
        self.kernel = kernel
        self.logger = logger
        self.cli = cli
        self.running = True

    def start(self):
        self.kernel.boot()

        worker = threading.Thread(target=self.loop, daemon=True)
        worker.start()

        try:
            self.cli.run()
        except KeyboardInterrupt:
            self.logger.info("CLI interrupted")

        self.running = False
        self.logger.info("Shutting down runtime...")

    def loop(self):
        while self.running:
            self.kernel.run_tick()
            time.sleep(1)
