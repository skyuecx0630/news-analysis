import json
import pandas as pd


class BaseFeed:
    def __init__(self, title, description) -> None:
        self.title = title
        self.description = description

    def __str__(self) -> str:
        return f"{self.title}\n{self.description}"


class Feed(BaseFeed):
    def __init__(self, title, description, link, published, media_content) -> None:
        super().__init__(title, description)
        self.link = link
        self.published = published
        self.media_content = media_content


class FeedSummary(Feed):
    def __init__(
        self, title, description, link, published, media_content, category, sentiment
    ) -> None:
        super().__init__(title, description, link, published, media_content)
        self.category = category
        self.sentiment = sentiment

    def __str__(self) -> str:
        return f"{self.category}, {self.sentiment}\n{self.title}\n{self.description}"


class FeedStorage:
    def __init__(self) -> None:
        pass

    def get_feed(self, feed_id):
        feed = self._get(feed_id)
        return FeedSummary(**feed) if feed else None

    def add_feed(self, feed):
        if self._get(feed.link):
            return False
        return self._put(feed)

    def _get(self, feed_id):
        raise NotImplementedError

    def _put(self, feed):
        raise NotImplementedError


class FileStorage(FeedStorage):
    def __init__(self, path) -> None:
        self.path = path
        self.database = None

    @property
    def database(self):
        if self._database is None:
            self._database = self._load_database()
        return self._database

    @database.setter
    def database(self, value):
        self._database = value

    def _load_database(self):
        with open(self.path, "r") as f:
            data = f.read() or "{}"
        return json.loads(data)

    def _save_database(self):
        with open(self.path, "w") as f:
            f.write(json.dumps(self.database, default=lambda x: x.__dict__))
        return True

    def _get(self, feed_id):
        if feed_id not in self.database:
            return None
        return self.database[feed_id]

    def _put(self, feed):
        self.database[feed.link] = feed
        self._save_database()
        return True


class CSVStorage(FeedStorage):
    def __init__(self, path) -> None:
        self.path = path
        self.database = None

    @property
    def database(self):
        if self._database is None:
            self._database = self._load_database()
        return self._database

    @database.setter
    def database(self, value):
        self._database = value

    def _load_database(self):
        try:
            df = pd.read_csv(self.path)
        except:
            df = pd.DataFrame()
        return df

    def _save_database(self):
        self.database.to_csv(self.path, index=False)
        return True

    def _get(self, feed_id):
        feed = self.database[self.database["link"] == feed_id]
        print(feed)
        return self.database[feed_id]

    def _put(self, feed):
        self.database[feed.link] = feed
        self._save_database()
        return True


if __name__ == "__main__":
    storage = CSVStorage("feed.csv")
    storage.get_feed("")
