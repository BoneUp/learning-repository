# python3
# -*- coding: utf-8 -*-
import time

from scrapy import Request, Spider
from zhihuuser.items import UserItem

import json


class ZhihuSpider(Spider):
    name = 'zhihu'
    start_user = 'cai-jun-98-37'  # the first user
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    # the attention member detials
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    # the followees list
    follow_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follow_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    # the followers list
    follower_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}'
    follower_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(
            self.user_url.format(
                user=self.start_user, include=self.user_query),
            self.user_parse)
        yield Request(
            self.follow_url.format(
                user=self.start_user,
                include=self.follow_query,
                offset=0,
                limit=20),
            callback=self.follow_parse)
        yield Request(
            self.follower_url.format(
                user=self.start_user,
                include=self.follower_query,
                offset=0,
                limit=20),
            callback=self.follower_parse)

    def user_parse(self, response):
        result = json.loads(response.text)
        # set up the Item for scrapy
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

        yield Request(
            self.follow_url.format(
                user=result.get('url_token'),
                include=self.follow_query,
                offset=0,
                limit=20), self.follow_parse)
        yield Request(
            self.follower_url.format(
                user=result.get('url_token'),
                include=self.follower_query,
                offset=0,
                limit=20), self.follower_parse)

    def follow_parse(self, response):
        time.sleep(3)
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(
                    self.user_url.format(
                        user=result.get('url_token'), include=self.user_query),
                    self.user_parse)

        if 'paging' in results.keys() and results.get('paging').get(
                'is_end') == 'false':
            next_page = results.get('paging').get('next')
            yield Request(next_page, self.follow_parse)

    def follower_parse(self, response):
        time.sleep(3)
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(
                    self.user_url.format(
                        user=result.get('url_token'), include=self.user_query),
                    self.user_parse)

        if 'paging' in results.keys() and results.get('paging').get(
                'is_end') == 'false':
            next_page = results.get('paging').get('next')
            yield Request(next_page, self.follower_parse)
