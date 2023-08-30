from logging import getLogger
import boto3

from feed import Feed, FeedSummary
from util import track_duration

logger = getLogger(__name__)
logger.setLevel("DEBUG")

CLASSIFIER_ENDPOINT_ARN = "arn:aws:comprehend:us-east-1:856210586235:document-classifier-endpoint/mynews-endpoint"


class MyNewsSummarizer:
    def __init__(self, source_language, target_language, boto_session) -> None:
        self.source_language = source_language
        self.target_language = target_language
        self.translate_client = boto_session.client("translate")
        self.comprehend_client = boto_session.client("comprehend")

    @track_duration
    def _translate_text(self, text):
        response = self.translate_client.translate_text(
            Text=text,
            SourceLanguageCode=self.source_language,
            TargetLanguageCode=self.target_language,
            Settings={"Formality": "FORMAL"},
        )

        logger.debug(response)
        return response["TranslatedText"]

    @track_duration
    def _detect_sentiment(self, text):
        response = self.comprehend_client.detect_sentiment(
            Text=text, LanguageCode=self.source_language
        )

        logger.debug(response)
        return response["Sentiment"]

    @track_duration
    def _classify_document(self, text, endpoint_arn):
        try:
            response = self.comprehend_client.classify_document(
                Text=text,
                EndpointArn=endpoint_arn,
            )
        except Exception as e:
            logger.error(e)
            return "CLASSIFICATION_FAIL"

        logger.debug(response)
        return response["Classes"][0]["Name"]

    @track_duration
    def summarize(self, news: Feed):
        title = news.title
        description = news.description

        translated_title = self._translate_text(title)
        translated_description = self._translate_text(description)

        text = f"{title}. {description}"
        sentiment = self._detect_sentiment(text)
        category = self._classify_document(text, CLASSIFIER_ENDPOINT_ARN)
        summary = FeedSummary(
            translated_title,
            translated_description,
            news.link,
            news.published,
            news.media_content,
            category,
            sentiment,
        )
        return summary


if __name__ == "__main__":
    session = boto3.Session()
    summarizer = MyNewsSummarizer("en", "ko", session)

    title = "India calls for fair trade rules"
    description = "Meanwhile, the German chancellor says there is no alternative to Russian supplies at the moment."
    news = Feed(title, description, None, None, None)

    print(str(summarizer.summarize(news)))
