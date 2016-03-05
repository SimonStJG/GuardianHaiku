# -*- coding: utf-8 -*-
"""
Tweeter for tweeting to twitter.
"""
from contextlib import contextmanager
import logging
import tweepy

logger = logging.getLogger(__name__)


# The consumer keys and access tokens care at https://dev.twitter.com/apps.
consumer_key = "zLbf5as3EJr0aY62V9r3o6YeZ"
consumer_secret = "DPFkZGdvn0zfUaupY0T93SCRkIEwqNHcuj7htYmwdhAPCH26HE"
access_token = "706073693659779072-08Q4xubUnXofs22BpbQJCIJlOrDEmN0"
access_token_secret = "p2BqIgbl9UhUeLFHRdPkDLzqHw4ABY76vd0VCf5Sy2ViZ"


@contextmanager
def tweeter():
    logger.info("Authorising with tweepy")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    logger.info("Authorised with tweepy")

    def tweet_function(message):
        logger.info("Tweeting message: {}".format(message))
        api.update_status(status=message)

    yield tweet_function
