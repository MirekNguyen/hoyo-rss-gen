from app.controllers import ConfigController, FeedController, WebScrapeController

config = ConfigController()
webscrape = WebScrapeController(config.data.get("url"))
print(webscrape.webscrape.has_error)
feed = FeedController(config, webscrape, config.args.output)
