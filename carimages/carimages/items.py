# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarimagesItem(scrapy.Item):
    # 文件夹名
    folder_name = scrapy.Field()
    # 图片链接
    img_url = scrapy.Field()
    # 图片名称
    img_name = scrapy.Field()
