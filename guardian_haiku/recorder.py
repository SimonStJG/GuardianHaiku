# -*- coding: utf-8 -*-
"""
Record found haiku.
"""
from __future__ import print_function

import json
import errno
import logging
from io import open

logger = logging.getLogger(__name__)


class Recorder(object):
    def __init__(self, filename):
        self._filename = filename

    def __enter__(self):
        try:
            with open(self._filename, mode="r") as f:
                self.haiku_list = json.load(f)["haiku_list"]
                logger.info("Opened {}, found haiku list: {}".format(
                    self._filename, self.haiku_list))
        except IOError as e:
            # If file doesn't exist
            if e.errno == errno.ENOENT:
                self.haiku_list = {}
                logger.info("File {} doesn't exist".format(self._filename))
            else:
                raise e
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self._filename, mode="w") as f:
            json.dump({"haiku_list": self.haiku_list}, f)
