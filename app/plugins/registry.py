from app.core.plugin_manager import PluginManager


class PluginRegistry:

    def __init__(self):
        self.manager = PluginManager()

    def load(self):
        self.manager.load()

    def start(self):
        self.manager.start()

    def plugins(self):
        return self.manager.plugins
