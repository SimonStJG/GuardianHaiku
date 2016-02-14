# -*- coding: utf-8 -*-

"""
Get haiku from the guardian website
"""
import datetime
import logging
from haikufinder import HaikuFinder
from recorder import Recorder
from scraper import extract_full_text, get_article_urls
from functools import reduce

LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

logger = logging.getLogger(__name__)


def find_haiku(haiku_finder, recorder, url):
    """Get haiku at URL"""
    try:
        return recorder.haiku_list[url]
    except KeyError:
        logger.info("Processing {}".format(url))

        text = extract_full_text(url)
        logger.debug("Found full text: {}".format(text))

        # Work around hyphenation bug
        text = [paragraph.replace("-", ",") for paragraph in text]

        haikus_found = [(haiku, url) for paragraph in text
                        for haiku in haiku_finder.find_haiku(paragraph)]

        if haikus_found:
            logger.info("Found Haiku: {}".format(haikus_found))
        else:
            logger.debug("No Haiku Found :(")

        recorder.haiku_list[url] = haikus_found

        return haikus_found


def flatten(list):
    """Why doesn't python have this :("""
    return reduce(lambda x, xs: x + xs, list, [])


if __name__ == "__main__":
    logfile_suffix = datetime.date.today().strftime("%Y-%m-%d")
    # Log at INFO level to scraper.log.
    logging.basicConfig(filename="scraper.{}.log".format(logfile_suffix),
                        level=logging.INFO,
                        format=LOG_FORMAT,
                        datefmt="%H:%M",
                        filemode='a')
    # Log at INFO level to console.
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT)
    console.setFormatter(formatter)
    logging.getLogger(__name__).addHandler(console)

    # Let's go!
    hf = HaikuFinder()
    with Recorder("haiku_found") as r:
        haiku = flatten([find_haiku(hf, r, url) for url in get_article_urls()])

    print(haiku)
