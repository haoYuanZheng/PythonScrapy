# -*- coding: utf-8 -*-
import scrapy
import pymysql
from qunaerone.items import QunaeroneItem


class MeishiSpider(scrapy.Spider):
    name = 'meishi'

    headers = {
        'authority': "travel.qunar.com",
        'cache-control': "max-age=0,no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3876.0 Safari/537.36",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'sec-fetch-site': "same-origin",
        'referer': "https://travel.qunar.com/p-cs300195-hangzhou-meishi",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9"
    }

    # 初始化，从数据库获取详情链接
    def __init__(self):
        try:
            self.conn = pymysql.Connect(host='localhost', user='root', password='13567651173', database='python',
                                        charset='utf8')
            cur = self.conn.cursor()
            sql = 'select detail_link,area from qnems_detail_url where is_download = 0 limit 1'
            cur.execute(sql)
            self.urls = list(cur.fetchall())
        except Exception as e:
            print("连接数据库出错,错误原因%s" % e)

    # 直接爬取详情页
    def start_requests(self):
        for url in self.urls:
            print("爬取链接::::::::" + url[0])
            item = QunaeroneItem()
            item['url'] = url[0]
            item['area'] = url[1]
            yield scrapy.Request(url=url[0], callback=self.step_one, headers=self.headers, meta={'item': item})

    # 详情页部分内容
    def step_one(self, response):
        item = response.meta['item']
        name = response.xpath('//*[@id="js_mainleft"]/div[@class="b_title clrfix"]/h1/text()').extract_first()
        total_score = response.xpath(
            '//*[@id="js_mainleft"]/div[4]/div/div[2]/div[1]/div[1]/span[1]/text()').extract_first()
        average_cost = response.xpath(
            '//*[@id="js_mainleft"]/div[4]/div/div[2]/div[1]/div[2]/div[2]/text()').extract_first()
        overview = response.xpath('//*[@id="gs"]/div[1]/p/text()').extract_first()
        address = response.xpath('//*[@id="gs"]/div[2]/div[1]/table/tr/td[1]/dl[1]/dd/span/text()').extract_first()
        phone_number = response.xpath('//*[@id="gs"]/div[2]/div[1]/table/tr/td[1]/dl[2]/dd/span/text()').extract_first()
        open_time = response.xpath('//*[@id="gs"]/div[2]/div[1]/table/tr/td[2]/dl[1]/dd/span/p/text()').extract_first()
        images = response.xpath('//*[@id="idNum"]/li/div[@class="imgbox"]/img/@src').extract()
        traffic = response.xpath('//*[@id="jtzn"]/div[2]/p/text()').extract_first()
        nearby_scenic = response.xpath('//*[@id="idContBox"]/ul[1]/li/a/@href').extract()
        nearby_food = response.xpath('//*[@id="idContBox"]/ul[2]/li/a/@href').extract()
        nearby_hotel = response.xpath('//*[@id="idContBox"]/ul[3]/li/a/@href').extract()
        nearby_shopping = response.xpath('//*[@id="idContBox"]/ul[4]/li/a/@href').extract()

        if name is not None:
            item['name'] = name
        if total_score is not None:
            item['total_score'] = total_score
        if average_cost is not None:
            item['average_cost'] = average_cost
        if overview is not None:
            item['overview'] = overview
        if address is not None:
            item['address'] = address
        if phone_number is not None:
            item['phone_number'] = phone_number
        if open_time is not None:
            item['open_time'] = open_time
        if images is not None:
            item['images'] = images
        if traffic is not None:
            item['traffic'] = traffic
        if nearby_scenic is not None:
            item['nearby_scenic'] = nearby_scenic
        if nearby_food is not None:
            item['nearby_food'] = nearby_food
        if nearby_hotel is not None:
            item['nearby_hotel'] = nearby_hotel
        if nearby_shopping is not None:
            item['nearby_shopping'] = nearby_shopping

        # 是否有翻页的评论需要爬取
        coments = []
        # 先爬取当前页
        for index in range(11):
            if index == 0:
                pass
            else:
                current = {}
                star = response.xpath(
                    '//*[@id="js_replace_box"]/div[2]/ul/li[$index]/div[1]/div[1]/div[2]/span/span/@class',
                    index=index).extract_first()
                content = "".join(
                    response.xpath('//*[@id="js_replace_box"]/div[2]/ul/li[$index]/div[1]/div[1]/div[3]/p/text()',
                                   index=index).extract())
                images = ",".join(response.xpath(
                    '//*[@id="js_replace_box"]/div[2]/ul/li[$index]/div[1]/div[1]/div[4]/div[1]/ul/li/a/@href',
                    index=index).extract())
                date = response.xpath(
                    '//*[@id="js_replace_box"]/div[2]/ul/li[$index]/div[1]/div[1]/div[5]/ul/li[1]/text()',
                    index=index).extract_first()
                if star is not None:
                    current['star'] = star[-1:]
                else:
                    break
                if content is not None:
                    current['content'] = content.replace("\r", "").replace(" ", "").replace("\n", "")
                if images is not None:
                    current['images'] = images
                if date is not None:
                    current['date'] = date
                coments.append(current)
        item['comments'] = coments
        next_page = response.xpath('//*[@id="js_replace_box"]/div[2]/div/a[@class="page next"]/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.step_two, headers=self.headers, meta={'item': item})

    # 下一页的评论
    def step_two(self, response):
        item = response.meta['item']
        coments = item['comments']
        # 先爬取当前页
        for index in range(11):
            if index == 0:
                pass
            else:
                current = {}
                star = response.xpath(
                    '//*[@id="js_replace_box"]/div[2]/ul/li[$index]/div[1]/div[1]/div[2]/span/span/@class',
                    index=index).extract_first()
                content = "".join(
                    response.xpath('//*[@id="js_replace_box"]/div[2]/ul/li[$index]/div[1]/div[1]/div[3]/p/text()',
                                   index=index).extract())
                images = ",".join(response.xpath(
                    '//*[@id="js_replace_box"]/div[2]/ul/li[$index]/div[1]/div[1]/div[4]/div[1]/ul/li/a/@href',
                    index=index).extract())
                date = response.xpath(
                    '//*[@id="js_replace_box"]/div[2]/ul/li[$index]/div[1]/div[1]/div[5]/ul/li[1]/text()',
                    index=index).extract_first()
                if star is not None:
                    current['star'] = star[-1:]
                else:
                    break
                if content is not None:
                    current['content'] = content.replace("\r", "").replace(" ", "").replace("\n", "")
                if images is not None:
                    current['images'] = images
                if date is not None:
                    current['date'] = date
                coments.append(current)
        item['comments'] = coments
        next_page = response.xpath('//*[@id="js_replace_box"]/div[2]/div/a[@class="page next"]/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.step_two, headers=self.headers, meta={'item': item})
        else:
            yield item
