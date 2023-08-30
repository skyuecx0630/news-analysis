from datetime import datetime, timedelta
from time import sleep

import feedparser
from feed import Feed


class NewsRSSParser:
    def __init__(self, rss_endpoint, interval=3) -> None:
        self.rss_endpoint = rss_endpoint
        self.feeds = None
        self.interval = timedelta(seconds=interval)
        self.last_update = datetime.now() - self.interval

    def _time_to_update(self):
        return datetime.now() - self.last_update >= self.interval

    def _parse(self):
        if self._time_to_update():
            self.feeds = feedparser.parse(self.rss_endpoint)
            self.last_update = datetime.now()
        return self.feeds

    def get_feeds(self):
        raise NotImplementedError


class CNNRSSParser(NewsRSSParser):
    def __init__(self, rss_endpoint, interval=3) -> None:
        super().__init__(rss_endpoint, interval)

    def _convert_published(self, text):
        return datetime.strptime(text, "%a, %d %b %Y %H:%M:%S GMT")

    def _convert_media_content(self, media_content):
        content = [
            content
            for content in media_content
            if content["width"] == "300" and content["height"] == "300"
        ]
        return content[0] if content else None

    def _convert_feed(self, feed):
        title = feed["title"]
        description = feed["summary"]
        link = feed["link"]
        published = feed["published"]

        if "media_content" in feed:
            media_content = self._convert_media_content(feed["media_content"])
        else:
            media_content = None
        return Feed(title, description, link, published, media_content)

    def get_feeds(self):
        self._parse()

        parsed_feeds = [self._convert_feed(feed) for feed in self.feeds["entries"]]
        return parsed_feeds


if __name__ == "__main__":
    RSS_ENDPOINT = "http://rss.cnn.com/rss/cnn_latest.rss"

    parser = CNNRSSParser(RSS_ENDPOINT, 3)
    feeds = parser.get_feeds()
    print(list(map(str, feeds))[0])
