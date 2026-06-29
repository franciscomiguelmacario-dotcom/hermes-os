from pathlib import Path
from dotenv import load_dotenv
import yaml
import os


class Config:

    def __init__(self):

        load_dotenv()

        self.env = dict(os.environ)

        config_file = Path("config/config.yaml")

        if config_file.exists():

            with open(config_file, "r") as f:

                self.yaml = yaml.safe_load(f)

        else:

            self.yaml = {}

    def get_env(self, key, default=None):

        return self.env.get(key, default)

    def get(self, section, key=None):

        if key is None:
            return self.yaml.get(section)

        return self.yaml.get(section, {}).get(key)
