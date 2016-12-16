# -*- coding:utf8 -*-
__author__ = 'gloria'


# 2016/12/15 16:41

class Utils:
    """
        按照指定分隔符将list转换为string
    """

    @staticmethod
    def list2string(list_obj, seperator):
        if list_obj is None:
            return ''
        result = ''
        for s in list_obj:
            result += (str(s).strip() + seperator)

        result = result[0:len(result) - 1]
        return result

    """
        对象转换为Dict
    """

    @staticmethod
    def convert_to_dict(obj):
        dict = {}
        dict.update(obj.__dict__)
        return dict
