# -*- coding: utf-8 -*-
"""
Get haiku from the guardian website
"""
import datetime
import logging
import os
from typing import Generator
from guardian_haiku.haiku_finder import find_haiku

from .scraper import extract_full_text, get_article_urls
from .utils import flatten


class Config(object):
    LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    LOG_DIR_ROOT = "/var/log/"
    LOGFILE_SUFFIX = datetime.date.today().strftime("%Y-%m-%d")
    DEFAULT_RSS_FEED_URL = "http://www.theguardian.com/uk/rss"

logger = logging.getLogger(__name__)


def process_url(guardian_url: str) -> Generator[str, None, None]:
    """Get haiku at URL"""
    logger.info("Processing {}".format(guardian_url))

    try:
        paragraphs = extract_full_text(guardian_url)
        logger.debug("Found full text: {}".format(paragraphs))
        for paragraph in paragraphs:
            haikus = find_haiku(paragraph)
            for haiku in haikus:
                logger.info("Found Haiku: {}".format(haiku))
                yield haiku
    except Exception:
        logger.exception("Failed on article: {}".format(guardian_url))


def setup_logging(log_dir_root: str, logfile_suffix: str) -> None:
    """
    Setup logging.

    log_dir_root should already exist, but if log_dir_root/guardian_haiku
    doesn't exist, create it.
    """
    if not os.path.isdir(log_dir_root):
        raise ValueError("Log directory root {} doesn't "
                         "exist".format(log_dir_root))

    log_dir = os.path.join(log_dir_root, "guardian_haiku")
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    # Log at DEBUG level to scraper.log.
    filename = "guardian_haiku.{}.log".format(logfile_suffix)
    logging.basicConfig(filename=os.path.join(log_dir, filename),
                        level=logging.DEBUG,
                        format=Config.LOG_FORMAT,
                        datefmt="%H:%M",
                        filemode='a')

    # Log at INFO level to console.
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(Config.LOG_FORMAT)
    console.setFormatter(formatter)
    logging.getLogger(__name__).addHandler(console)


def main(log_dir_root: str=Config.LOG_DIR_ROOT,
         logfile_suffix: str=Config.LOGFILE_SUFFIX,
         rss_feed_url: str=Config.DEFAULT_RSS_FEED_URL) -> str:
    """Entry Point"""
    setup_logging(log_dir_root, logfile_suffix)
    logger.info("guardian_haiku running with \n"
                "log_dir_root: {log_dir_root} \n"
                "logfile_suffix: {logfile_suffix} \n".format(**locals()))
    try:
        return list(flatten(process_url(url) for url in get_article_urls(rss_feed_url)))
    except Exception as e:
        logger.fatal("guardian_haiku terminated", exc_info=True)
        raise
