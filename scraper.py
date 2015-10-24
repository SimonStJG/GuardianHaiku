#!/usr/bin/env python2
"""
Content Scraper for the guardian website.

Functions to scrape the guardian website and return their full text.
"""
from __future__ import print_function
import logging
from lxml import etree, html
from StringIO import StringIO
from unidecode import unidecode
import requests
from haikufinder import HaikuFinder

LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
logger = logging.getLogger(__name__)


def find_haiku(haiku_finder, url):
    logger.info("Processing {}".format(url))

    """Download article from url and return any haiku contained within."""
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

    return haikus_found


def get_article_urls():
    """Get all of the article urls of all articles on the guardian RSS feed."""
    raw_xml = unidecode(requests.get("http://www.theguardian.com/uk/rss").text)
    tree = etree.parse(StringIO(raw_xml))
    # There are single 'rss' and 'channel' element, all stories appear under
    #  channel as 'item' elements.
    return [elem.text for elem in tree.xpath('/rss/channel/item/link')]


def extract_full_text(url):
    """
    Extract the full text from the guardian article at url.

    Attempts to convert the unicode output to ASCII using unidecode.  I haven't
    seen this cause problems, yet.
    """
    page = requests.get(url)
    tree = html.fromstring(page.text)
    paragraphs = [etree.tostring(paragraph,
                                 method="text",
                                 encoding='unicode').strip()
                  for paragraph in
                  tree.xpath(r'//div[@itemprop="articleBody"]/p')]
    normalised_text = [unidecode(p) for p in paragraphs]
    return normalised_text


def flatten(list):
    """Why doesn't python have this :("""
    return reduce(lambda x, xs: x + xs, list, [])


if __name__ == "__main__":
    # Log at DEBUG level to scraper.log.
    logging.basicConfig(filename='scraper.log',
                                 level=logging.DEBUG,
                                 format=LOG_FORMAT,
                                 datefmt='%m-%d %H:%M',
                                 filemode='a')
    # Log at INFO level to console.
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT)
    console.setFormatter(formatter)
    logging.getLogger(__name__).addHandler(console)

    # Let's go!
    haiku = flatten([find_haiku(HaikuFinder(), url)
                     for url in get_article_urls()])

    print(haiku)
