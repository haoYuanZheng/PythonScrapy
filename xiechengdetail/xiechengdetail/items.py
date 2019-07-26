# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiechengdetailItem(scrapy.Item):
    # 店名+人均消费+店铺类型+地址+电话+营业时间
    name = scrapy.Field()
    address = scrapy.Field()
    # averageCost = scrapy.Field()
    # type = scrapy.Field()
    # phoneNumber = scrapy.Field()
    # openTime = scrapy.Field()
    # 简介
    introduce = scrapy.Field()
    # 特色美食
    special_food = scrapy.Field()
    # 附近酒店
    nearby_hotel = scrapy.Field()
    # 附近景点
    nearby_scenic = scrapy.Field()
    # 附近餐馆
    nearby_resturant = scrapy.Field()
    # 附近团购
    nearby_group_buy = scrapy.Field()
