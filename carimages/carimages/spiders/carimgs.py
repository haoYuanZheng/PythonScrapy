# -*- coding: utf-8 -*-
import scrapy
from carimages.items import CarimagesItem


class CarimgsSpider(scrapy.Spider):
    name = 'carimgs'

    headers = {
        'Connection': "keep-alive",
        'Cache-Control': "max-age=0",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3860.5 Safari/537.36",
        'Sec-Fetch-Mode': "navigate",
        'Sec-Fetch-User': "?1",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Sec-Fetch-Site': "cross-site",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache"
    }

    def start_requests(self):
        url = 'https://www.chevrolet.com.cn/camaro6/'
        yield scrapy.Request(url=url, callback=self.step_one, headers=self.headers)

    def step_one(self, response):
        headUrl = 'https://www.lincoln.com.cn/content/dam/lincoln/cn/l_cn_zh/nameplate/continental/360/Exterior/'
        colors = ['铂钻白/', '狂想蓝/', '瀚星灰/', '曜晶黑/']
        img_url_dict = {}
        for color in colors:
            for index in range(37):
                if index != 0:
                    # if index < 10:
                    #     img_name = "000" + str(index) + ".jpg"
                    # else:
                    #     img_name = "00" + str(index) + ".jpg"
                    img_name = str(index) + ".jpg"
                    img_url = headUrl + color + img_name
                    img_url_dict[img_name] = img_url
                else:
                    continue
            item = CarimagesItem()
            item['img_url'] = img_url_dict
            item['folder_name'] = color.replace("/", "")
            item['img_name'] = img_name
            yield item
