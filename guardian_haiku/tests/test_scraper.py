# -*- coding: utf-8 -*-
import pytest
from guardian_haiku.scraper import extract_full_text, get_article_urls
from guardian_haiku.guardian_haiku import Config


class TestGuardian(object):
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
        urls = get_article_urls(rss_feed_url=Config.guardian_rss_feed_url)
        assert len(urls) > 10


class TestIndependent(object):
    def test_extract_full_text(self):
        """Extract full text of a known link and check first paragraph"""
        full_text = extract_full_text("http://www.independent.co.uk/news/uk/crime/two-arrested-after-stolen-fire-"
                                      "engine-crashed-into-cars-and-homes-a6914071.html")
        assert (full_text[0] ==
                "A pensioner and a teenager have been arrested after a fire engine was stolen from a fire station and "
                "crashed into nearby cars and houses.")

    def test_get_article_urls(self):
        """Check something is returned by get_article_urls"""
        urls = get_article_urls(rss_feed_url=Config.independent_rss_feed_url)
        assert len(urls) > 10


class TestTelegraph(object):
    @pytest.mark.xfail
    def test_extract_full_text(self):
        """Extract full text of a known link and check first paragraph"""
        full_text = extract_full_text("http://www.telegraph.co.uk/culture/film/oscars/12177476/Oscars-2016-academy-"
                                      "award-winners-list-leonardo-dicaprio.html")
        assert (full_text[0] ==
                "A pensioner and a teenager have been arrested after a fire engine was stolen from a fire station and "
                "crashed into nearby cars and houses.")

    def test_get_article_urls(self):
        """Check something is returned by get_article_urls"""
        urls = get_article_urls(rss_feed_url=Config.telegraph_rss_feed_url)
        assert len(urls) > 10


class TestMailOnline(object):
    @pytest.mark.xfail
    def test_extract_full_text(self):
        """Extract full text of a known link and check first paragraph"""
        full_text = extract_full_text("http://www.dailymail.co.uk/wires/pa/article-3477877/Fire-engine-stolen-"
                                      "station-driven-cars-houses.html?ITO=1490&ns_mchannel=rss&ns_campaign=1490")
        assert (full_text[0] ==
                "A pensioner and a teenager have been arrested after a fire engine was stolen from a fire station and "
                "crashed into nearby cars and houses.")

    def test_get_article_urls(self):
        """Check something is returned by get_article_urls"""
        urls = get_article_urls(rss_feed_url=Config.mailonline_rss_feed_url)
        assert len(urls) > 10
