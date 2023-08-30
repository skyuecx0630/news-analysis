from rss import CNNRSSParser
from summarizer import MyNewsSummarizer
from feed import FileStorage

from time import sleep
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    CNN_RSS_ENDPOINT = "http://rss.cnn.com/rss/cnn_latest.rss"
    rss_parser = CNNRSSParser(CNN_RSS_ENDPOINT, interval=3)
    storage = FileStorage("./feed.txt")

    session = boto3.Session()
    summarizer = MyNewsSummarizer("en", "ko", session)

    feeds = rss_parser.get_feeds()
    # for feed in feeds:
    #     print(sum([len(str(feed)) for feed in feeds]))
    #     summary = summarizer.summarize(feed)
    #     print(summary)
    for feed in feeds:
        existing_feed = storage.get_feed(feed.link)
        if existing_feed:
            print(existing_feed)
            print()
            continue
        summary = summarizer.summarize(feed)
        storage.add_feed(summary)
        print(summary)
        print()
        sleep(3)
