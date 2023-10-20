from feedgen.feed import FeedGenerator


class Feed:
    def __init__(self, feed_id, feed_title, feed_subtitle, feed_link_href):
        self.fg = FeedGenerator()
        self.fg.id(feed_id)
        self.fg.title(feed_title)
        self.fg.subtitle(feed_subtitle)
        self.fg.link(href=feed_link_href, rel="self")
        self.fg.language("en")
        pass
