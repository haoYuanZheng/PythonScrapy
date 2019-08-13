# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QunaertwoItem(scrapy.Item):
    # 名称
    name = scrapy.Field()
    # 总分
    total_score = scrapy.Field()
    # 概述
    overview = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 营业时间
    open_time = scrapy.Field()
    # 图片
    images = scrapy.Field()
    # 交通
    traffic = scrapy.Field()
    # 附近景点
    nearby_scenic = scrapy.Field()
    # 附近美食
    nearby_food = scrapy.Field()
    # 附近酒店
    nearby_hotel = scrapy.Field()
    # 附近购物
    nearby_shopping = scrapy.Field()
    # 评论
    comments = scrapy.Field()

    # 爬取链接
    url = scrapy.Field()
    # 地区
    area = scrapy.Field()
