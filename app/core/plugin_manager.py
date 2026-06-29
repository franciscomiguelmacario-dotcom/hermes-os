from app.core.plugin_loader import PluginLoader


class PluginManager:

    def __init__(self, logger=None):
        self.logger = logger
        self.plugins = {}

    def load(self):
        loader = PluginLoader(self.logger)
        self.plugins = loader.load()

    def start(self):
        for name, plugin in self.plugins.items():
            if hasattr(plugin, "start"):
                plugin.start()

    def get(self, name):
        return self.plugins.get(name)
