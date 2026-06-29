from rich.console import Console
from datetime import datetime

console = Console()


class Logger:

    def log(self, level, message):
        console.print(
            f"[{datetime.now().strftime('%H:%M:%S')}] [{level}] {message}"
        )

    def info(self, msg):
        self.log("INFO", msg)

    def success(self, msg):
        self.log("OK", msg)

    def warning(self, msg):
        self.log("WARN", msg)

    def error(self, msg):
        self.log("ERROR", msg)

