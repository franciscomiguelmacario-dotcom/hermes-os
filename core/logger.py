from datetime import datetime

class Logger:

    def _log(self, level, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [{level}] {message}")

    def info(self, message):
        self._log("INFO", message)

    def success(self, message):
        self._log("OK", message)

    def warning(self, message):
        self._log("WARN", message)

    def error(self, message):
        self._log("ERROR", message)
