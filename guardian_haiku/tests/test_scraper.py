# -*- coding: utf-8 -*-
from guardian_haiku.guardian_haiku import Config
from guardian_haiku.scraper import extract_full_text, get_article_urls


class TestFunctional(object):
    """Functional tests for scraper"""

    def test_extract_full_text(self):
        """Extract full text of a known link and check first paragraph"""
        full_text = extract_full_text("http://www.theguardian.com/"
                                      "world/2016/feb/13/russia-warns-of-new-"
                                      "cold-war-amid-syria-accusations-munich")
        assert (full_text[0] ==
                "The Russian prime minister has said the world is slipping "
                "into a \u201cnew cold war\u201d after European leaders condemned "
                "his country\u2019s airstrikes on Syria and called on Vladimir "
                "Putin to end them as a precursor for peace negotiations.")

    def test_get_article_urls(self):
        """Check something is returned by get_article_urls"""
        urls = get_article_urls(rss_feed_url=Config.DEFAULT_RSS_FEED_URL)
        assert len(urls) > 10
