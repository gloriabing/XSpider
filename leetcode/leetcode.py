# -*- coding:utf8 -*-
from base_utils.log_util import LoggerHelper
import base_utils.http_util as http
import json

__author__ = 'gloria'
# 2017/3/2 14:23


class LeetCode:

    def __init__(self):
        self.base_url = "https://leetcode.com/api/problems/algorithms/"

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.98 Safari/537.36 '
        }
        self._name = 'leetcode algorithms'
        self._logger = LoggerHelper(self._name, '../logs/leetcode.log', True).get_logger()
        self._console = LoggerHelper('console', '', False).get_logger()

    def fetch_body(self, url):
        body = http.HttpUtil.get_response_body_by_get(url, "utf-8", self.headers)
        return body

    def parse(self, body):
        stat_status_pairs = json.loads(body)['stat_status_pairs']
        questions = []

        try:
            for stat_pair in stat_status_pairs:
                question = Question()
                question.question_id = stat_pair['stat']['question_id']
                question.question_title = stat_pair['stat']['question__title']
                question.question_title_slug = stat_pair['stat']['question__title_slug']
                question.url = 'https://leetcode.com/problems/' + question.question_title_slug + '/'
                question.question_article_live = stat_pair['stat']['question__article__live']
                if question.question_article_live is None:
                    question.question_article_live = False

                question.difficulty = stat_pair['difficulty']['level']
                question.paid_only = stat_pair['paid_only']
                question.status = stat_pair['status']
                if question.status is None:
                    question.status = '0'

                question.total_acs = stat_pair['stat']['total_acs']
                question.total_submitted = stat_pair['stat']['total_submitted']

                # print(question)

                questions.append(question)

        except Exception as e:
            print(e)
            return 0

        return questions

    def run(self):
        body = self.fetch_body(self.base_url)
        questions = self.parse(body)

        for question in questions:
            print(question)
            print("---------------------------------------------------------------------------------------------------")


class Question:
    url = ''
    question_id = ''
    question_title_slug = ''
    question_title = ''
    question_article_live = 'false'
    difficulty = ''
    paid_only = 'false'
    status = ''
    total_acs = ''
    total_submitted = ''

    def __str__(self):
        return 'url :' + self.url + ', \n' + \
               '问题id :' + str(self.question_id) + ', \n' + \
               '标题 :' + self.question_title + ', \n' + \
               '标题slug :' + self.question_title_slug + ', \n' + \
               '文档 :' + str(self.question_article_live) + ', \n' + \
               '难度 :' + str(self.difficulty) + ', \n' + \
               '是否付费 :' + str(self.paid_only) + ', \n' + \
               '提交总数 : ' + str(self.total_submitted) + ', \n' + \
               '通过总数 : ' + str(self.total_acs) + ', \n' + \
               '状态 :' + self.status


if __name__ == '__main__':
    spider = LeetCode()
    spider.run()
