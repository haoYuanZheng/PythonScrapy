# -*- coding: utf-8 -*-
import scrapy
from xiecheng.items import XiechengItem


# 携程美食、购物点列表页爬取
class MeishigouwuSpider(scrapy.Spider):
    name = 'meishigouwu'
    page_success_log = []

    headers = {
        'authority': "travel.qunar.com",
        'cache-control': "max-age=0,no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.19 Safari/537.36",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'sec-fetch-site': "same-origin",
        'referer': "https://travel.qunar.com/p-cs300195-hangzhou",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9"
    }

    # nextPageHead = "https://you.ctrip.com"
    url = 'https://travel.qunar.com/p-cs300184-quzhou-gouwu?page='
    index = 1

    def start_requests(self):
        # url = 'https://you.ctrip.com/restaurantlist/hangzhou14.html'
        yield scrapy.Request(url=self.url + str(self.index), callback=self.second)

    def second(self, response):
        detailUrl = response.xpath('/html/body/div[2]/div/div[6]/div[1]/div[1]/div[2]/ul/li/a/@href').extract()
        self.page_success_log.append(self.index)
        self.index += 1
        # 爬取下一页
        if self.index <= 200:
            yield scrapy.Request(url=self.url + str(self.index), callback=self.second)
        # 存储链接 已成功下载【杭州hz、宁波nb、绍兴sx、嘉兴jx、温州wz、湖州huzhou、金华jh、舟山zs、台州tz、丽水ls、衢州qz】
        if detailUrl is not None:
            for url in detailUrl:
                item = XiechengItem()
                item['detail_link'] = url
                item['area'] = 'qz'
                yield item
