# -*- coding: utf-8 -*-
"""
Content Scraper for the guardian website.

Functions to scrape the guardian website and return their full text.
"""
from __future__ import print_function
import logging
from lxml import etree, html
import requests
from typing import List

logger = logging.getLogger(__name__)


def get_article_urls(rss_feed_url: str) -> List[str]:
    """Get all of the article urls of all articles on the guardian RSS feed."""
    response = requests.get(rss_feed_url)
    response.raise_for_status()
    raw_xml = response.text

    # Bizarrely, etree.fromstring doesn't actually operate on strings, so we
    # must encode raw_xml, only to immediately decode it afterwards,
    tree = etree.fromstring(raw_xml.encode(encoding="utf-8"),
                            parser=etree.XMLParser(encoding='utf-8'))
    # All stories appear under channel as 'item' elements.
    return [elem.text for elem in tree.xpath('/rss/channel/item/link')]


def extract_full_text(url: str) -> List[str]:
    """ Extract the full text from the guardian article at url."""
    response = requests.get(url)
    response.raise_for_status()

    html_tree = html.fromstring(response.text)
    paragraphs = [etree.tostring(paragraph,
                                 method="text",
                                 encoding='unicode').strip()
                  for paragraph in
                  html_tree.xpath(r'//div[@itemprop="articleBody"]/p')]
    return paragraphs
