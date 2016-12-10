# -*- coding:utf8 -*-
import requests

__author__ = 'gloria'
# 2016/12/9 15:35

'''
    网络请求工具类
'''


class HttpUtil:

    @staticmethod
    def get_response_body_by_get(url, charset, headers):
        response = requests.get(url, headers=headers)
        return response.content.decode(charset)

    @staticmethod
    def get_response_body_by_post(url, charset, params):
        response = requests.post(url, data=params)
        return response.content.decode(charset)
