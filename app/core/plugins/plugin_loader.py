import os
import importlib


class PluginLoader:

    def __init__(self, logger):
        self.logger = logger
        self.plugins = []

    def load(self, brain, bus, memory):

        path = "app/plugins"

        for file in os.listdir(path):

            if file.endswith(".py") and file != "__init__.py":

                module_name = f"app.plugins.{file[:-3]}"

                module = importlib.import_module(module_name)

                if hasattr(module, "register"):

                    plugin = module.register(brain, bus, memory)

                    self.plugins.append(plugin)

                    self.logger.info(f"Plugin loaded: {file}")
