# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuangyeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 公司名称
    company_name = scrapy.Field()
    # 公司介绍
    company_introduction = scrapy.Field()
    # 联系人
    contact_person = scrapy.Field()
    # 联系人电话
    contact_tel = scrapy.Field()
    # 所在地、成立时间等信息
    company_address = scrapy.Field()
