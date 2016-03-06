# -*- coding: utf-8 -*-

from guardian_haiku.scraper import guardian_scraper, independent_scraper, telegraph_scraper, mailonline_scraper


class TestGuardian(object):
    def test_extract_full_text(self):
        """Extract full text of a known link and check first paragraph"""
        full_text = guardian_scraper.extract_full_text("http://www.theguardian.com/world/2016/feb/13/russia-warns-of-"
                                                       "new-cold-war-amid-syria-accusations-munich")
        assert (full_text[0] ==
                "The Russian prime minister has said the world is slipping "
                "into a \u201cnew cold war\u201d after European leaders condemned "
                "his country\u2019s airstrikes on Syria and called on Vladimir "
                "Putin to end them as a precursor for peace negotiations.")

    def test_get_article_urls(self):
        """Check something is returned by get_article_urls"""
        urls = guardian_scraper.get_article_urls()
        assert len(urls) > 10


class TestIndependent(object):
    def test_extract_full_text(self):
        """Extract full text of a known link and check first paragraph"""
        full_text = independent_scraper.extract_full_text("http://www.independent.co.uk/news/uk/crime/two-arrested-"
                                                          "after-stolen-fire-engine-crashed-into-cars-and-homes-"
                                                          "a6914071.html")
        assert (full_text[0] ==
                "A pensioner and a teenager have been arrested after a fire engine was stolen from a fire station and "
                "crashed into nearby cars and houses.")

    def test_get_article_urls(self):
        """Check something is returned by get_article_urls"""
        urls = independent_scraper.get_article_urls()
        assert len(urls) > 10


class TestTelegraph(object):
    def test_extract_full_text(self):
        """Extract full text of a known link and check first paragraph"""
        full_text = telegraph_scraper.extract_full_text("http://www.telegraph.co.uk/news/uknews/law-and-order/12184708/"
                                                        "Britains-cold-call-king-young-tech-geek-who-lives-with-"
                                                        "his-mother.html")
        assert (full_text[0] ==
                "He calls himself “moosey_man” on dating websites and describes himself as a “hopeless romantic”, who "
                "enjoys playing the guitar and the occasional game of tennis. Louis Kidd, a 27-year-old who still "
                "lives at home with his mother, may seem harmless enough.")

    def test_get_article_urls(self):
        """Check something is returned by get_article_urls"""
        urls = telegraph_scraper.get_article_urls()
        assert len(urls) > 10


class TestMailOnline(object):
    def test_extract_full_text(self):
        """Extract full text of a known link and check first paragraph"""
        full_text = mailonline_scraper.extract_full_text("http://www.dailymail.co.uk/news/article-3478947/The-EU-"
                                                         "fuelling-Hitler-worshippers-bad-national-security-"
                                                         "Michael-Gove-claims-new-escalation-Brexit-battle.html")
        assert (full_text[0] ==
                "The EU has fuelled the far right so it is stronger than at any time Hitler's rise to power in the "
                "1930s, Michael Gove warned today.")

    def test_get_article_urls(self):
        """Check something is returned by get_article_urls"""
        urls = mailonline_scraper.get_article_urls()
        assert len(urls) > 10
