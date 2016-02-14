# -*- coding: utf-8 -*-
"""
Content Scraper for the guardian website.

Functions to scrape the guardian website and return their full text.
"""
from __future__ import print_function
import logging
from lxml import etree, html
import requests

logger = logging.getLogger(__name__)


def get_article_urls():
    """Get all of the article urls of all articles on the guardian RSS feed."""
    raw_xml = requests.get("http://www.theguardian.com/uk/rss").text
    # Bizarrely, etree.fromstring doesn't actually operate on strings, so we
    # must encode raw_xml, only to immediately decode it afterwards,
    tree = etree.fromstring(raw_xml.encode(encoding="utf-8"),
                            parser=etree.XMLParser(encoding='utf-8'))
    # All stories appear under channel as 'item' elements.
    return [elem.text for elem in tree.xpath('/rss/channel/item/link')]


def extract_full_text(url):
    """Extract the full text from the guardian article at url."""
    page = requests.get(url)
    html_tree = html.fromstring(page.text)
    paragraphs = [etree.tostring(paragraph,
                                 method="text",
                                 encoding='unicode').strip()
                  for paragraph in
                  html_tree.xpath(r'//div[@itemprop="articleBody"]/p')]
    return paragraphs
