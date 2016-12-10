# -*- coding:utf8 -*-
from datetime import date, datetime

import postgresql.driver as pg_driver

__author__ = 'gloria'
# 2016/12/9 15:55

'''
    PostgreSQL 操作工具类
    doc ：http://python.projects.pgfoundry.org/docs/1.1/driver.html
'''


class PgConfig:

    __config__ = {
        'user': 'postgres',
        'password': 'admin',
        'host': 'localhost',
        'port': 5432,
        'database': 'postgres'
    }

    @staticmethod
    def get_connection():
        return pg_driver.connect(**PgConfig.__config__)


