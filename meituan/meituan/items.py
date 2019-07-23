# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanItem(scrapy.Item):
    # 美食名称
    meal_name = scrapy.Field()
    # 美食类型
    meal_type = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 支持条款
    support_items = scrapy.Field()
    # 标签
    label = scrapy.Field()
    # 店铺地址
    company = scrapy.Field()
    # 备注
    comment = scrapy.Field()

    # 爬取详情链接
    # url = scrapy.Field()
