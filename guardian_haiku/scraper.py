# -*- coding: utf-8 -*-
"""
Content Scraper for the guardian website.

Functions to scrape the guardian website and return their full text.
"""
from __future__ import print_function
import logging
from lxml import etree, html
from StringIO import StringIO
import requests

from unidecode import unidecode

logger = logging.getLogger(__name__)


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
