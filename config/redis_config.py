# -*- coding:utf8 -*-
import redis

__author__ = 'gloria'


# 2016/12/14 22:01
class RedisConfig:

    __config__ = {
        'host': 'localhost',
        'port': 6333,
        'db': 0
    }

    @staticmethod
    def get_connection():
        return redis.StrictRedis(**RedisConfig.__config__)
