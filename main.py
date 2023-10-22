from app.controllers import *

config = ConfigController()
webscrape = None
for route_name, url in config.data.get("routes").items():
    if config.args.route != route_name:
        continue
    base_name = route_name.replace("_url", "")
    controller_name = (
        "".join(word.capitalize() for word in base_name.split("_")) + "Controller"
    )
    controller = globals().get(controller_name)
    if controller and callable(
        controller
    ):  # Check if the function exists and is callable
        webscrape = controller(url)
    else:
        raise ValueError(f"No controller found for route '{route_name}'")
if webscrape is None:
    raise ValueError(
        f"No valid controller found for the provided route: '{config.args.route}'"
    )

feed = FeedController(
    config,
    webscrape.getFeedConfig(),
    webscrape.webscrape.has_error,
    webscrape.webscrape.error_message,
    config.args.output,
)
