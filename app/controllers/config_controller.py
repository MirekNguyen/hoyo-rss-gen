import argparse
from app.models.config import Config


class ConfigController:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Create RSS feed from web scraping")
        parser.add_argument("-o", "--output", help="Specify output file name", required=True)
        parser.add_argument("-c", "--config", help="Specify configuration file location", default='config/config.json')
        parser.add_argument("--route", help="Specify the route", required=True)
        self.args = parser.parse_args()
        config = Config(self.args.config)
        self.data = config.data
        self.validate_route(self.args.route)

    def validate_route(self, route):
        available_routes = self.data.get("routes", {})
        if route not in available_routes:
            print(f"Invalid route: '{route}'. Available routes are:")
            for available_route in available_routes:
                print(f"- {available_route}")
            exit(1)
