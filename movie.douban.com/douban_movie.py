# -*- coding:utf8 -*-
import time

import re
from bs4 import BeautifulSoup

import base_utils.http_util as http
import json
import base_utils.redis_util as redis
from base_utils.common_util import Utils

from base_utils.log_util import LoggerHelper

__author__ = 'gloria'


# 2016/12/12 15:38


class DoubanMovie:
    def __init__(self):
        self.base_url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend" \
                        "&page_limit=20&page_start=([page_start])"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.98 Safari/537.36 '
        }
        self._name = 'douban movie'
        self.redis_conn = redis.RedisUtil()
        self._logger = LoggerHelper(self._name, '../logs/douban_movie_info.log', True).get_logger()
        self._console = LoggerHelper('console', '', False).get_logger()

    def fetch_body(self, url):
        body = http.HttpUtil.get_response_body_by_get(url, "utf-8", self.headers)
        return body

    def generate_fetch_url(self, page_num):
        page_start = page_num * 20
        return self.base_url.replace('([page_start])', str(page_start))

    '''
        抓取列表页资源
    '''

    def parse_catalog(self, start_page):
        url = self.generate_fetch_url(start_page)
        body = self.fetch_body(url)
        subjects = json.loads(body)['subjects']

        movies = []

        try:
            for subject in subjects:
                movie = Movie()
                movie.rate = subject['rate']
                movie.title = subject['title']
                movie.url = subject['url']
                movie.id = subject['id']
                movie.cover = subject['cover']
                movie.cover_x = subject['cover_x']
                movie.cover_y = subject['cover_y']
                movies.append(movie)
        except Exception as e:
            print(e)
            return 0

        return movies

    def parse_content(self, movie):
        body = self.fetch_body(movie.url)
        body_dom = BeautifulSoup(body, 'html.parser')
        content = body_dom.find(id='content')
        movie.name = content.find('span', attrs={'property': 'v:itemreviewed'}).text

        try:
            year = content.find('span', attrs={'class': 'year'}).text
        except:
            self._logger.error('detail info parse error, url is %s ' % movie.url)
        try:
            movie.year = re.compile('([\d]+)').search(year).group(1)
        except:
            self._logger.error('year parse error, url is %s ' % movie.url)

        info = content.find(id='info')

        try:
            movie.directors = [x.strip() for x in re.compile('导演: ([\s\S]*?)\n').search(info.text).group(1).split("/")]
        except:
            self._logger.error('directors parse error, url is %s ' % movie.url)

        try:
            movie.writes = [x.strip() for x in re.compile('编剧: ([\s\S]*?)\n').search(info.text).group(1).split("/")]
        except:
            self._logger.error('writes parse error, url is %s ' % movie.url)

        try:
            movie.main_actors = [x.strip() for x in re.compile('主演: ([\s\S]*?)\n').search(info.text).group(1).split("/")]
        except:
            self._logger.error('main_actors parse error, url is %s ' % movie.url)

        try:
            movie.genres = [x.strip() for x in re.compile('类型: ([\s\S]*?)\n').search(info.text).group(1).split("/")]
        except:
            self._logger.error('genres parse error, url is %s ' % movie.url)

        try:
            movie.language = [x.strip() for x in re.compile('语言: ([\s\S]*?)\n').search(info.text).group(1).split("/")]
        except:
            self._logger.error('language parse error, url is %s ' % movie.url)

        try:
            movie.pub_date = [x.strip() for x in re.compile('上映日期: ([\s\S]*?)\n').search(info.text).group(1).split("/")]
        except:
            self._logger.error('pub_date parse error, url is %s ' % movie.url)

        try:
            movie.alias = [x.strip() for x in re.compile('又名: ([\s\S]*?)\n').search(info.text).group(1).split("/")]
        except:
            self._logger.error('alias parse error, url is %s ' % movie.url)

        try:
            movie.official_site = re.compile('官方网站: ([\s\S]*?)\n').search(info.text).group(1)
        except:
            self._logger.error('official_site parse error, url is %s ' % movie.url)

        try:
            movie.region = re.compile('制片国家/地区: ([\s\S]*?)\n').search(info.text).group(1)
        except:
            self._logger.error('region parse error, url is %s ' % movie.url)

        try:
            movie.run_time = re.compile('片长: ([\s\S]*?)\n').search(info.text).group(1)
        except:
            self._logger.error('run_time parse error, url is %s ' % movie.url)

        try:
            IMDb = re.compile('IMDb链接: ([\s\S]*?)\n').search(info.text).group(1)
            movie.IMDb = 'http://www.imdb.com/title/' + IMDb
        except:
            self._logger.error('IMDb parse error, url is %s ' % movie.url)

        return movie

    def run(self):
        start_page = 0

        while True:
            movies = self.parse_catalog(start_page)
            for movie in movies:
                url = movie.url
                r = self.redis_conn.set_if_absent(url)
                if r:  # 新资源
                    movie = self.parse_content(movie)
                    # self._logger.info(Utils.convert_to_dict(movie))
                    self._console.info(Utils.convert_to_dict(movie))
                else:  # 已存在
                    continue
                time.sleep(1)

            if movies is None or len(movies) == 0:
                # 没有更多内容
                break
            else:
                start_page += 1
            time.sleep(3)


class Movie:
    rate = 0.0  # 评分
    title = ''  # 列表页名称
    name = ''  # 详情页名称，全称
    url = ''
    cover = ''
    id = ''
    cover_x = 0
    cover_y = 0
    year = 1900  # 年代
    directors = []  # 导演
    writers = []  # 编剧
    main_actors = []  # 主演
    genres = []  # 类型
    official_site = ''  # 官方网站
    region = ''  # 地区
    language = []  # 语言
    pub_date = []  # 上映日期
    run_time = ''  # 片长
    alias = []  # 别名
    IMDb = ''  # IMDb

    def __str__(self):
        return '资源id :' + self.id + ', \n' + \
               '评分 :' + str(self.rate) + ', \n' + \
               '电影名称 :' + self.title + ', \n' + \
               '电影全称 :' + self.name + ', \n' + \
               '链接 :' + self.url + ', \n' + \
               '封面图 :' + self.cover + ', \n' + \
               '年代 :' + self.year + ', \n' + \
               '导演 :' + Utils.list2string(self.directors, ',') + ', \n' + \
               '编剧 :' + Utils.list2string(self.writers, ',') + ', \n' + \
               '主演 :' + Utils.list2string(self.main_actors, ',') + ', \n' + \
               '类型 :' + Utils.list2string(self.genres, ',') + ', \n' + \
               '官方网站 :' + self.official_site + ', \n' + \
               '地区 :' + self.region + ', \n' + \
               '语言 :' + Utils.list2string(self.language, ',') + ', \n' + \
               '上映日期 :' + Utils.list2string(self.pub_date, ',') + ', \n' + \
               '片长 :' + self.run_time + ', \n' + \
               '又名 :' + Utils.list2string(self.alias, ',') + ', \n' + \
               'IMDb链接 :' + self.IMDb


if __name__ == '__main__':
    spider = DoubanMovie()
    spider.run()
