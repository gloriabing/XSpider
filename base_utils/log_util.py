# -*- coding:utf8 -*-
import logging
import logging.config

import sys

__author__ = 'gloria'


# 2016/12/16 14:24

class LoggerHelper:
    def __init__(self, log_name, file_name, flag):
        self._flag = log_name
        self._formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._logger = logging.getLogger(log_name)
        if flag:
            handler = logging.FileHandler(file_name)
        else:
            handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(self._formatter)
        self._logger.setLevel('INFO')
        self._logger.addHandler(handler)

    def get_logger(self):
        return self._logger

