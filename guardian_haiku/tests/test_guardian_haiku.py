# -*- coding: utf-8 -*-
import os
from unittest import mock
import tempfile

import pytest
import requests

from guardian_haiku.guardian_haiku import main, Config

test_resources = os.path.join(os.path.dirname(__file__), "resources")


def mock_requests_get(url):
    """Mock for requests.get"""
    article_url = "http://www.theguardian.com/politics/2016/feb/21/" \
                  "cameron-boris-johnson-brexit-nigel-farage-george-galloway-uk"
    if url == Config.DEFAULT_RSS_FEED_URL:
        with open(os.path.join(test_resources, "sample_rss.xml")) as f:
            text = f.read()
    elif url == article_url:
        with open(os.path.join(test_resources, "sample_article.html")) as f:
            text = f.read()
    else:
        raise ValueError("Mock Requests can't handle url: {}".format(url))

    mock_response = mock.MagicMock()
    mock_response.text = text
    return mock_response


@pytest.yield_fixture
def logfile_directory():
    with tempfile.TemporaryDirectory() as tmpdir_name:
        yield tmpdir_name


@pytest.fixture
def logfile_suffix():
    return "functional_test"


def test_logging(monkeypatch, logfile_directory, logfile_suffix):
    monkeypatch.setattr(requests, "get", mock_requests_get)
    main(log_dir_root=logfile_directory,
         logfile_suffix=logfile_suffix)

    with open("{logfile_directory}/guardian_haiku/guardian_haiku."
              "{logfile_suffix}.log".format(logfile_directory=logfile_directory,
                                            logfile_suffix=logfile_suffix)) as f:
        first_log_line = f.readline()
        assert "guardian_haiku running" in first_log_line, ("Expected \"guardian_haiku\" running in first line of "
                                                            "log output, but was \n{}".format(first_log_line))


def test_mainline(monkeypatch, logfile_directory, logfile_suffix):
    monkeypatch.setattr(requests, "get", mock_requests_get)
    assert list(main(log_dir_root=logfile_directory,
                logfile_suffix=logfile_suffix)) == ["Greedy yellow birds. Sing the muddy riverbank. On a window sill."]
