import logging
import tweepy

from textwrap import wrap
from tweepy.models import Media

from config import config

logger = logging.getLogger(f"zug_foi_watchdog.{__name__}")


class TweetService:

    def __init__(self):
        self.api = tweepy.Client(
            consumer_key=config.get("TWITTER_API_KEY"),
            consumer_secret=config.get("TWITTER_API_SECRET"),
            access_token=config.get("TWITTER_ACCESS_TOKEN"),
            access_token_secret=config.get("TWITTER_ACCESS_SECRET")
        )

    def upload_media(self, filename) -> Media | None:
        if config.get("DEV"):
            logger.debug("Not uploading media since program is running in development mode")
            return None

        logger.debug(f"Uploading media with filename {filename}")

        return self.api.media_upload(filename=filename)

    def tweet_thread(self, text, lat=None, lon=None, media_filename=None, extra_parts=None, answer_to=None) -> list[str]:
        if extra_parts is None:
            extra_parts = []
        logger.debug("Sending tweet (as thread if necessary)")

        media = None

        if media_filename:
            media = self.upload_media(media_filename)
            logger.debug(f"Uploaded media: {media}")

        parts = [text]

        # This way of checking the tweet length is not how Twitter does it, but good enough for our purposes
        if len(text) > 280:
            logger.debug("Text longer than 280 chars, wrapping it")
            raw_wrapped = wrap(text, 270, replace_whitespace=False)
            parts = list(map(lambda part_tuple: f"{part_tuple[1]} {part_tuple[0] + 1}/{len(raw_wrapped)}",
                             enumerate(raw_wrapped)))

        parts.extend(extra_parts)
        last_status = answer_to
        tweet_ids = []

        for index, part in enumerate(parts):
            logger.debug(f"Tweeting part {index + 1}/{len(parts)}")
            tweet_params = {'text': part}

            if index == 0 and media:
                tweet_params['media_ids'] = [media.media_id]

            if last_status:
                tweet_params['in_reply_to_tweet_id'] = last_status

            logger.debug(f'Tweeting with params: {tweet_params}')

            # The below return values are not adapted to the v2 endpoint, but we don't need it for this small project.
            if config.get("DEV"):
                logger.debug("Not sending tweet since program is running in development mode")
                return ["TWEET_ID1", "TWEET_ID2", "TWEET_ID3"]
            else:
                last_status = self.api.create_tweet(**tweet_params).id
                tweet_ids.append(last_status)

        return tweet_ids


tweet_service = TweetService()
