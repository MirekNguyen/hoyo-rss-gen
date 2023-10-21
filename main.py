from app.controllers import ConfigController, FeedController, WebScrapeController, HsrCodesController

config = ConfigController()
# webscrape = WebScrapeController(config.data.get("url"))
webscrape = HsrCodesController(config.data.get("hsr_codes_url"))
feed = FeedController(config, webscrape, config.args.output)
