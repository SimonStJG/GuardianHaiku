# -*- coding: utf-8 -*-
"""
Get haiku from the guardian website
"""
import datetime
import logging
import os
from typing import Generator, List
from .dictionary import Dictionary
from .haiku_finder import find_haiku
from .scraper import extract_full_text, get_article_urls


class Config(object):
    log_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    log_dir_root = "/var/log/"
    logfile_suffix = datetime.date.today().strftime("%Y-%m-%d")
    guardian_rss_feed_url = "http://www.theguardian.com/uk/rss"
    independent_rss_feed_url = "http://www.independent.co.uk/rss"
    telegraph_rss_feed_url = "http://www.telegraph.co.uk/rss"
    mailonline_rss_feed_url = "http://www.dailymail.co.uk/articles.rss"

logger = logging.getLogger(__name__)


def process_url(guardian_url: str,
                dictionary: Dictionary) -> Generator[str, None, None]:
    """Get haiku at URL"""
    logger.info("Processing {}".format(guardian_url))

    try:
        paragraphs = extract_full_text(guardian_url)
        logger.debug("Found full text: {}".format(paragraphs))
        for paragraph in paragraphs:
            haikus = find_haiku(paragraph, dictionary)
            for haiku in haikus:
                logger.info("Found Haiku: {}".format(haiku))
                yield haiku
    except Exception:
        logger.exception("Failed on article: {}".format(guardian_url))


def process_rss_feed(rss_feed_url: str,
                     dictionary: Dictionary) -> Generator[str, None, None]:
    logger.info("Processing RSS Feed: {}".format(rss_feed_url))
    for url in get_article_urls(rss_feed_url):
        yield from process_url(url, dictionary)


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
                        format=Config.log_format,
                        datefmt="%H:%M",
                        filemode='a')

    # Log at INFO level to console.
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(Config.log_format)
    console.setFormatter(formatter)
    logging.getLogger(__name__).addHandler(console)


def main(log_dir_root: str=Config.log_dir_root,
         logfile_suffix: str=Config.logfile_suffix,
         rss_feed_url: str=Config.guardian_rss_feed_url) -> List[str]:
    """Entry Point"""
    setup_logging(log_dir_root, logfile_suffix)
    logger.info("guardian_haiku running with \n"
                "log_dir_root: {log_dir_root} \n"
                "logfile_suffix: {logfile_suffix} \n".format(**locals()))
    dictionary = Dictionary()
    try:
        result = list(process_rss_feed(rss_feed_url, dictionary))
        print(dictionary.unknown_words)  # TODO remove
        return result
    except Exception as e:
        logger.fatal("guardian_haiku terminated", exc_info=True)
        raise
