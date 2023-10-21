import locale
from datetime import datetime

import pytz

from app.models.feed import Feed


class FeedController():
    def __init__(self, config, feedConfig, has_error, error_message, output_file):
        feed = Feed(
            config.data.get("feed_id"),
            config.data.get("feed_title"),
            config.data.get("feed_subtitle"),
            config.data.get("feed_link_href"),
        )
        if (has_error):
            self.__buildErrorFeed(config, error_message, output_file, feed)
        else:
            self.__buildFeed(config, feedConfig, output_file, feed)

    def __buildFeed(self, config, data, output_file, feed):
        for item in data:
            fe = feed.fg.add_entry()
            fe.id(item.id)
            fe.title(item.title)
            fe.link(href=item.link, replace=True)
            fe.description(item.description)
            locale.setlocale(locale.LC_TIME, config.data.get("locale"))
            fe.pubDate(pytz.timezone(config.data.get("timezone")).localize(item.pubDate))
        feed.fg.rss_str(pretty=True)
        feed.fg.rss_file(output_file)

    def __buildErrorFeed(self, config, error_message, output_file, feed):
        locale.setlocale(locale.LC_TIME, config.data.get("locale"))
        fe = feed.fg.add_entry()
        fe.title("Error " + datetime.now().strftime("%y/%m/%d %H:%M:%S"))
        fe.id("error_" + datetime.now().strftime("%y%m%d"))
        fe.link(href="", replace=True)
        fe.description(error_message)
        fe.pubDate(
            pytz.timezone(config.data.get("timezone")).localize(datetime.now())
        )
        feed.fg.rss_str(pretty=True)
        feed.fg.rss_file(output_file)

