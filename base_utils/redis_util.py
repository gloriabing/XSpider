# -*- coding:utf8 -*-
import config.redis_config as redis_config
import hashlib

__author__ = 'gloria'


# 2016/12/14 22:00
class RedisUtil:

    def __init__(self):
        self.connection = redis_config.RedisConfig.get_connection()

    '''
        set存储
    '''

    def set(self, key, value):
        self.connection.set(key, value)

    '''
        根据key取出对应的值
    '''

    def get(self, key):
        return self.connection.get(key)

    '''
        向指定队列中存储对象
    '''

    def lpush(self, key, value):
        self.connection.lpush(key, value)

    '''
        从指定队列中取出一个对象
    '''

    def rpop(self, key):
        return self.connection.rpop(key)

    '''
        从队列中取出指定范围的对象
    '''

    def lrange(self, key, start, end):
        return self.connection.lrange(key, start, end)

    '''
        判读key不存在再进行存储
        :return
                false --> 已存在，不进行存储
                true  --> 不存在，添加key
    '''

    def set_if_absent(self, key):
        m = hashlib.md5(key.encode(encoding='utf-8'))
        md5_key = m.hexdigest().lower()
        if self.connection.exists(md5_key) is True:
            return False
        else:
            self.set(md5_key, "")
            return True

    '''
        批量删除key
        *tup : 元组类型参数
                例如：
                    list = {"abc", "123"}
                    tup = tuple(list)
                    delete(*tup)
                    或者
                    tup = ("abc", "123")
                    delete(*tup)
        :return
                成功删除的个数
    '''

    def delete(self, *tup):
        return self.connection.delete(*tup)

    '''
        根据pattern查出对应keys
    '''

    def keys(self, pattern):
        key_list = self.connection.keys(pattern)
        result_list = []
        for key in key_list:
            result_list.append(key.decode("utf-8"))
        return result_list
