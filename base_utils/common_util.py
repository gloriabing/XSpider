# -*- coding:utf8 -*-
__author__ = 'gloria'


# 2016/12/15 16:41

class Utils:

    @staticmethod
    def list2string(list_obj, seperator):
        if list_obj is None:
            return ''
        result = ''
        for s in list_obj:
            result += (str(s) + seperator)

        result = result[0:len(result) - 1]
        return result
