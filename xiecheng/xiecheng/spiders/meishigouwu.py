# -*- coding: utf-8 -*-
import scrapy
from xiecheng.items import XiechengItem

# 携程美食、购物点列表页爬取
class MeishigouwuSpider(scrapy.Spider):
    name = 'meishigouwu'
    page_success_log = []

    # allowed_domains = ['you.trip.com']
    # start_urls = ['http://you.trip.com/']
    # headers = {
    #     'authority': "you.ctrip.com",
    #     'cache-control': "max-age=0,no-cache",
    #     'upgrade-insecure-requests': "1",
    #     'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3854.3 Safari/537.36",
    #     'sec-fetch-mode': "navigate",
    #     'sec-fetch-user': "?1",
    #     'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    #     'sec-fetch-site': "same-origin",
    #     'referer': "https://you.ctrip.com/fooditem/hangzhou14.html",
    #     'accept-encoding': "gzip, deflate, br",
    #     'accept-language': "zh-CN,zh;q=0.9"
    # }

    headers = {
        'authority': "you.ctrip.com",
        'cache-control': "max-age=0,no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3854.3 Safari/537.36",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'sec-fetch-site': "same-origin",
        'referer': "https://you.ctrip.com/goods/hangzhou14.html",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
    }

    nextPageHead = "https://you.ctrip.com"

    def start_requests(self):
        # url = 'https://you.ctrip.com/restaurantlist/hangzhou14.html'
        url = 'https://you.ctrip.com/shoppinglist/hangzhou14.html'
        yield scrapy.Request(url=url, callback=self.second, headers=self.headers)

    def second(self, response):
        detailUrl = response.xpath(
            '/html/body/div[4]/div/div[2]/div/div[3]/div[@class="list_mod2"]/div[1]/a/@href').extract()
        nextPageUrl = response.xpath(
            '/html/body/div[4]/div/div[2]/div/div[3]/div[16]/div/a[@class="nextpage"]/@href').extract_first()
        currentPage = response.xpath(
            '/html/body/div[4]/div/div[2]/div/div[3]/div[16]/div/a[@class="current"]/text()').extract_first()
        self.page_success_log.append(currentPage)
        # 爬取下一页
        if nextPageUrl is not None:
            yield scrapy.Request(url=self.nextPageHead + nextPageUrl, callback=self.second, headers=self.headers)
        # 存储链接
        if detailUrl is not None:
            for url in detailUrl:
                item = XiechengItem()
                item['detail_link'] = self.nextPageHead + url
                yield item
