import argparse
from app.models.config import Config


class ConfigController:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Create RSS feed from web scraping")
        parser.add_argument("-o", "--output", help="Specify output file name", required=True)
        parser.add_argument("-c", "--config", help="Specify configuration file location", default='config/config.json')
        self.args = parser.parse_args()
        config = Config(self.args.config)
        self.data = config.data
