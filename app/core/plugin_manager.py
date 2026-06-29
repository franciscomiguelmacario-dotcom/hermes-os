import importlib
import pkgutil
from pathlib import Path

from app.core.logger import Logger
from app.core.plugin import HermesPlugin


class PluginManager:

    def __init__(self):

        self.logger = Logger()
        self.plugins = []

    def load(self):

        skills = Path("app/skills")

        if not skills.exists():
            return

        for module in pkgutil.iter_modules([str(skills)]):

            name = module.name

            try:

                plugin_module = importlib.import_module(
                    f"app.skills.{name}.plugin"
                )

                for obj in vars(plugin_module).values():

                    if (
                        isinstance(obj, type)
                        and issubclass(obj, HermesPlugin)
                        and obj is not HermesPlugin
                    ):

                        plugin = obj()

                        self.plugins.append(plugin)

                        self.logger.success(
                            f"Plugin carregado: {plugin.name}"
                        )

            except Exception as e:

                self.logger.error(f"{name}: {e}")

    def start(self):

        for plugin in self.plugins:

            plugin.start()
