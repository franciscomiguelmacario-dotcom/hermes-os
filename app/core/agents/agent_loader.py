import os
import importlib
import inspect

from app.core.agents.base_agent import BaseAgent


class AgentLoader:

    def __init__(self, logger):
        self.logger = logger

    def load(self, brain, memory, bus):
        path = "app/core/agents"
        loaded = {}

        skip = {
            "__init__.py",
            "base_agent.py",
            "agent_loader.py"
        }

        for file in os.listdir(path):
            if not file.endswith(".py") or file in skip:
                continue

            module_name = f"app.core.agents.{file[:-3]}"
            module = importlib.import_module(module_name)

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if obj is BaseAgent:
                    continue

                if issubclass(obj, BaseAgent):
                    agent_name = file[:-3]

                    agent = obj(
                        agent_name,
                        memory,
                        self.logger,
                        bus,
                        brain
                    )

                    loaded[agent_name] = agent
                    self.logger.info(f"Agent auto-loaded: {agent_name}")

        return loaded
