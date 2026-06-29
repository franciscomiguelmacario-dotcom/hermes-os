from app.core.plugin import HermesPlugin


class SystemPlugin(HermesPlugin):

    name = "System"
    version = "0.1"

    def start(self):
        print("✓ Plugin System iniciado")

    def stop(self):
        print("Plugin System parado")
