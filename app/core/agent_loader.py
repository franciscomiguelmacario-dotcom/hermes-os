import os
import importlib


class AgentLoader:

    def __init__(self, logger):
        self.logger = logger

    def load(self, memory, logger):
        agents = {}

        path = "app/core/agents"

        for file in os.listdir(path):
            if file.endswith(".py") and file != "__init__.py":

                module_name = f"app.core.agents.{file[:-3]}"
                module = importlib.import_module(module_name)

                for attr in dir(module):
                    obj = getattr(module, attr)

                    if isinstance(obj, type) and attr.endswith("Agent"):

                        name = attr.replace("Agent", "").lower()

                        try:
                            agents[name] = obj(memory, logger)
                            self.logger.info(f"Agent carregado: {name}")
                        except:
                            try:
                                agents[name] = obj(logger)
                                self.logger.info(f"Agent carregado: {name}")
                            except:
                                pass

        return agents
