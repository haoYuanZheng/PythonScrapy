# -*- coding: utf-8 -*-
import scrapy


class MsgwxqSpider(scrapy.Spider):
    name = 'msgwxq'
    allowed_domains = ['you.trip.com']
    start_urls = ['http://you.trip.com/']

    def parse(self, response):
        pass
