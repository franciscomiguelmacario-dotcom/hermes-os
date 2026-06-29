from core.logger import Logger
from core.plugin_manager import PluginManager

def main():
    logger = Logger()

    logger.info("Hermes OS v0.1")
    logger.success("Core iniciado")

    plugins = PluginManager()
    plugins.load()

    logger.success("Sistema operacional")

if __name__ == "__main__":
    main()
