# -*- coding: utf-8 -*-
import os
from unittest import mock
import tempfile

import pytest
import requests

from guardian_haiku.poet import main

test_resources = os.path.join(os.path.dirname(__file__), "resources")


def test_logging(logfile_directory, logfile_suffix):
    list(main(log_dir_root=logfile_directory, logfile_suffix=logfile_suffix))

    with open("{logfile_directory}/guardian_haiku/guardian_haiku."
              "{logfile_suffix}.log".format(logfile_directory=logfile_directory,
                                            logfile_suffix=logfile_suffix)) as f:
        first_log_line = f.readline()
        assert "guardian_haiku running" in first_log_line, ("Expected \"guardian_haiku\" running in first line of "
                                                            "log output, but was \n{}".format(first_log_line))


@pytest.mark.xfail
def test_mainline(logfile_directory, logfile_suffix):
    result = list(main(log_dir_root=logfile_directory, logfile_suffix=logfile_suffix))
    assert result == [("Guardian", ["Greedy yellow birds. Sing the muddy riverbank. On a window sill."])]


@pytest.fixture(autouse=True)
def mock_requests(monkeypatch):
    """Mock out requests.get"""
    def mock_requests_get(url):
        guardian_article_url = "http://www.theguardian.com/politics/2016/feb/21/" \
                               "cameron-boris-johnson-brexit-nigel-farage-george-galloway-uk"
        independent_article_url = "http://www.independent.co.uk/news/world/asia/mh370-two-years-after-the-" \
                                  "disappearance-of-malaysia-airlines-jet-and-still-no-answer-for-grieving-" \
                                  "a6915756.html"
        mailonline_article_url = "http://www.dailymail.co.uk/wires/ap/article-3486401/Senate-shoots-resolution-" \
                                 "against-F-16-sale-Pakistan.html?ITO=1490&amp;ns_mchannel=rss&amp;ns_campaign=1490"
        telegraph_article_url = "http://telegraph.feedsportal.com/c/32726/f/579330/s/4e2c2384/sc/13/l/0L0Stelegraph" \
                                "0O0Cnews0Cuknews0C12190A4830CPolice0Erelease0Eshocking0Efootage0Eto0Eshow0Eeffect" \
                                "0Eof0Elegal0Ehighs0Bhtml/story01.htm"

        if "theguardian" in url and "rss" in url:
            text = get_test_resource("guardian_rss.xml")
        elif "independent" in url and "rss" in url:
            text = get_test_resource("independent_rss.xml")
        elif "telegraph" in url and "rss" in url:
            text = get_test_resource("telegraph_rss.xml")
        elif "mailonline" in url and "rss" in url:
            text = get_test_resource("mailoneline_rss.rss")
        elif url == guardian_article_url:
            text = get_test_resource("guardian_article.html")
        elif url == independent_article_url:
            text = get_test_resource("independent_article.html")
        elif url == mailonline_article_url:
            text = get_test_resource("mailonline_article.html")
        elif url == telegraph_article_url:
            text = get_test_resource("telegraph_article.html")
        else:
            raise ValueError("Mock Requests can't handle url: {}".format(url))

        mock_response = mock.MagicMock()
        mock_response.text = text
        return mock_response

    def get_test_resource(resource_name):
        with open(os.path.join(test_resources, resource_name)) as f:
            return f.read()

    monkeypatch.setattr(requests, "get", mock_requests_get)


@pytest.yield_fixture
def logfile_directory():
    with tempfile.TemporaryDirectory() as tmpdir_name:
        yield tmpdir_name


@pytest.fixture
def logfile_suffix():
    return "functional_test"
