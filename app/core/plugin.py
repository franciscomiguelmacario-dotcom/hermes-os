from abc import ABC, abstractmethod


class HermesPlugin(ABC):

    name = "Plugin"
    version = "0.1"

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
