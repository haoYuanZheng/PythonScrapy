# -*- coding: utf-8 -*-
import scrapy
import pymysql
import random
import re
import json
from xiechengdetail.items import XiechengdetailItem


class MsgwxqSpider(scrapy.Spider):
    name = 'msgwxq'
    headerOne = {
        'authority': "you.ctrip.com",
        'cache-control': "max-age=0,no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3854.3 Safari/537.36",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'sec-fetch-site': "same-origin",
        'referer': "https://you.ctrip.com/restaurantlist/hangzhou14.html",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9"
    }

    headerTwo = {
        'authority': "you.ctrip.com",
        'cache-control': "max-age=0,no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3860.5 Safari/537.36",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'sec-fetch-site': "same-origin",
        'referer': "https://you.ctrip.com/shoppinglist/hangzhou14/s0-p5.html",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9"
    }

    nextPageHead = "https://you.ctrip.com"

    # 初始化，从数据库获取详情链接
    def __init__(self):
        try:
            self.conn = pymysql.Connect(host='localhost', user='root', password='13567651173', database='python',
                                        charset='utf8')
            cur = self.conn.cursor()
            # sql = 'select detail_link from xqms_detail_url'
            sql = 'select detail_link from xqgw_url_single'
            cur.execute(sql)
            self.urls = list(cur.fetchall())
            random.shuffle(self.urls)
        except Exception as e:
            print("连接数据库出错,错误原因%s" % e)

    # 直接爬取详情页
    def start_requests(self):
        for url in self.urls:
            print("爬取链接::::::::" + url[0])
            yield scrapy.Request(url=url[0], callback=self.step_one, headers=self.headerTwo)

    # 第一个详情页
    def step_one(self, response):
        item = XiechengdetailItem()
        # name = response.xpath('/html/body/div[2]/div[2]/div/div[1]/h1/text()').extract_first()
        name = response.xpath('/html/body/div[2]/div[2]/div/div[1]/h1/a/text()').extract_first()
        if name is not None:
            item['name'] = name
        # address = response.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[4]/span[2]/text()').extract_first()
        address = response.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li/span[2]/text()').extract_first()
        if address is not None:
            address = address.replace("\n", "").replace(" ", "")
        item['address'] = address
        # introduce = response.xpath(
        #     '/html/body/div[3]/div/div[1]/div[3]/div[1]/div[@itemprop="description"]/text()').extract_first()
        introduce = response.xpath('/html/body/div[3]/div/div[1]/div[3]/div[1]/div[1]/div/div/text()').extract_first()
        if introduce is not None:
            introduce = introduce.replace("\r\n", "").replace(" ", "")
        item['introduce'] = introduce
        # special_food = response.xpath(
        #     '/html/body/div[3]/div/div[1]/div[3]/div[@class="detailcon"]/div[2]/p/text()').extract_first()
        special_food = response.xpath('/html/body/div[3]/div/div[1]/div[3]/div[2]/div/ul/li/dl/dt/text()').extract()
        if special_food is not None:
            special_food = "|".join(special_food)
        #     special_food = special_food.replace("\r\n", "").replace(" ", "")
        item['special_food'] = special_food
        # averageCost = response.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/span[2]/em/text()').extract_first()
        # if averageCost is not None:
        #     item['averageCost'] = averageCost
        # type = "、".join(response.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[2]/span[2]/dd/a/text()').extract())
        # if type is not None:
        #     item['type'] = type
        # phoneNumber = response.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/span[2]/text()').extract_first()
        # if phoneNumber is not None:
        #     item['phoneNumber'] = phoneNumber
        # openTime = response.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[5]/span[2]/text()').extract_first()
        # if address is not None:
        #     item['openTime'] = openTime
        #
        pageTwo = response.xpath('//*[@id="jieshao"]/div/ul/li[2]/h2/a/@href').extract_first()
        if pageTwo is not None:
            yield scrapy.Request(url=self.nextPageHead + pageTwo, callback=self.step_two, meta={'item': item},
                                 headers=self.headerTwo)

    # 第二个tab页
    def step_two(self, response):
        # res = re.findall(r"<script.*?>.*?</script>", response.text, re.I | re.S | re.M)[15]
        res = re.findall(r"<script.*?>.*?</script>", response.text, re.I | re.S | re.M)[14]
        data = re.findall('\[.*?\]', res)
        if data is not None:
            item = response.meta['item']
            item['nearby_resturant'] = json.loads(data[0])
            item['nearby_hotel'] = json.loads(data[1])
            item['nearby_scenic'] = json.loads(data[2])
        endPage = response.xpath('//*[@id="zhusu"]/div/ul/li[5]/h2/a/@href').extract_first()
        if endPage is not None:
            yield scrapy.Request(url=self.nextPageHead + endPage, callback=self.step_three, meta={'item': item},
                                 headers=self.headerTwo)
        else:
            item['nearby_group_buy'] = None
            yield item

    # 团购tab页
    def step_three(self, response):
        item = response.meta['item']
        nearbyGroupBuy = response.xpath('/html/body/div[3]/div/div[1]/div[3]/ul/li/dl/dt/text()').extract()
        if nearbyGroupBuy is not None:
            nearbyGroupBuy = "|".join(nearbyGroupBuy).replace(" ", "").replace("\r\n", "")
        item['nearby_group_buy'] = nearbyGroupBuy
        yield item
