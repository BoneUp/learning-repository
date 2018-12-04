# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """    
    is_followed = Field()
    avatar_url_template = Field()
    user_type = Field()
    answer_count = Field()
    is_following = Field()
    url = Field()
    url_token = Field()
    id = Field()
    allow_message = Field()
    articles_count = Field()
    is_blocking = Field()
    name = Field()
    headline = Field()
    badgetype = Field()
    badgedescription = Field()
    introduction = Field()
    topicavatar_url = Field()
    topicname = Field()
    topicurl = Field()
    topictype = Field()
    excerpt = Field()
    topicid = Field()
    badge2type = Field()
    badge2description = Field()
    is_vip = Field()
    is_advertiser = Field()
    avatar_url = Field()
    is_org = Field()
    gender = Field()
    follower_count = Field()
    employments = Field()
    datatype = Field()
    """
    is_followed = Field()
    avatar_url_template = Field()
    user_type = Field()
    answer_count = Field()
    is_following = Field()
    url = Field()
    url_token = Field()
    id = Field()
    allow_message = Field()
    articles_count = Field()
    is_blocking = Field()
    name = Field()
    headline = Field()
    badge = Field()
    vip_info = Field()
    is_advertiser = Field()
    avatar_url = Field()
    is_org = Field()
    gender = Field()
    follower_count = Field()
    employments = Field()
    type = Field()
