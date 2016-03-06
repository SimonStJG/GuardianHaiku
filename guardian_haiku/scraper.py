# -*- coding: utf-8 -*-
"""
Content Scraper for the guardian website.

Functions to scrape the guardian website and return their full text.
"""
from collections import namedtuple
import logging
from lxml import etree, html
import requests
from typing import List

logger = logging.getLogger(__name__)


def get_article_urls(rss_feed_url: str, rss_xpath: str) -> List[str]:
    """Get all of the article urls of all articles at rss_feed_url."""
    response = requests.get(rss_feed_url)
    response.raise_for_status()
    raw_xml = response.text

    # Bizarrely, etree.fromstring doesn't actually operate on strings, so we
    # must encode raw_xml, only to immediately decode it afterwards,
    tree = etree.fromstring(raw_xml.encode(encoding="utf-8"), parser=etree.XMLParser(encoding='utf-8'))
    # All stories appear under channel as 'item' elements.
    return [elem.text for elem in tree.xpath(rss_xpath)]


def extract_full_text(url: str, paragraph_xpath: str) -> List[str]:
    """ Extract the full text from the article at url."""
    response = requests.get(url)
    response.raise_for_status()

    html_tree = html.fromstring(response.text)
    return [etree.tostring(paragraph, method="text", encoding='unicode').strip()
            for paragraph in html_tree.xpath(paragraph_xpath)]


scraper_type = namedtuple("scraper", ("name", "get_article_urls", "extract_full_text"))
scrapers = []


def scraper(name: str, rss_feed_url: str, rss_xpath: str, paragraph_xpath: str) -> scraper_type:
    s = scraper_type(name,
                     lambda: get_article_urls(rss_feed_url, rss_xpath),
                     lambda url: extract_full_text(url, paragraph_xpath))
    scrapers.append(s)
    return s

guardian_scraper = scraper(name="Guardian",
                           rss_feed_url="http://www.theguardian.com/uk/rss",
                           rss_xpath='/rss/channel/item/link',
                           paragraph_xpath=r'//div[@itemprop="articleBody"]/p')

independent_scraper = scraper(name="Indepedent",
                              rss_feed_url="http://www.independent.co.uk/rss",
                              rss_xpath='/rss/channel/item/link',
                              paragraph_xpath=r'//div[@itemprop="articleBody"]/p')

mailonline_scraper = scraper(name="Mail Online",
                             rss_feed_url="http://www.dailymail.co.uk/articles.rss",
                             rss_xpath='/rss/channel/item/link',
                             paragraph_xpath=r'//div[@itemprop="articleBody"]/p/font')

# TODO This doesn't seem to work for all articles - investigate?
telegraph_scraper = scraper(name="Telegraph",
                            rss_feed_url="http://www.telegraph.co.uk/rss",
                            rss_xpath='/rss/channel/item/link',
                            paragraph_xpath=r'//div[@itemprop="articleBody"]/div/p')
