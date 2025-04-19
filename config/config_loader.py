import yaml
import configparser
from pathlib import Path

class ConfigLoader:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent

    def load_api_config(self):
        with open(self.base_path/'config/api_config.yaml') as f:
            return yaml.safe_load(f)

    def load_model_config(self):
        with open(self.base_path/'config/model_config.yaml') as f:
            return yaml.safe_load(f)

    def setup_logging(self):
        import logging.config
        logging.config.fileConfig(
            self.base_path/'config/logging_config.ini',
            disable_existing_loggers=False
        )
