# -*- coding: utf-8 -*-
import scrapy
from xiecheng.items import XiechengItem
from lxml import etree
import json


# 携程美食、购物点列表页爬取
class MeishigouwuSpider(scrapy.Spider):
    name = 'meishigouwu'
    page_success_log = []

    headers = {
        'Connection': "keep-alive",
        'Cache-Control': "max-age=0",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3876.0 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Referer': "http://www.lvmama.com/lvyou/d-hangzhou100.html",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'If-Modified-Since': "Tue, 13 Aug 2019 02:30:00 GMT",
        'cache-control': "no-cache",
        'Postman-Token': "38e7fefa-3d39-42d9-9de1-89dff9d9f60d"
    }

    # nextPageHead = "https://you.ctrip.com"
    url = 'http://www.lvmama.com/lvyou/dest_good/AjaxGetStore?search_key=&dest_id=117&request_uri=/lvyou/shop/d-lishui117.html&type=shop&page='
    index = 1

    def start_requests(self):
        # url = 'https://you.ctrip.com/restaurantlist/hangzhou14.html'
        yield scrapy.Request(url=self.url + str(self.index), callback=self.second)

    def second(self, response):
        data = json.loads(response.text).get('data').get('html')
        html = etree.HTML(data)
        detailUrl = html.xpath('//*[@id="list_sotret"]/div[1]/dl/dt/a/@href')
        self.page_success_log.append(self.index)
        self.index += 1
        # 爬取下一页
        if self.index <= 1:
            yield scrapy.Request(url=self.url + str(self.index), callback=self.second)
        # 存储链接 已成功下载【杭州hz、宁波nb、绍兴sx、嘉兴jx、温州wz-失败、湖州huzhou、金华jh-失败、舟山zs、台州tz-失败、丽水ls、衢州qz-失败】
        # 西塘xt 临安la 桐庐tl 普陀山pts 乌镇wuzhen 海盐hy 千岛湖qdh
        if detailUrl is not None:
            for url in detailUrl:
                item = XiechengItem()
                item['detail_link'] = url
                item['area'] = 'ls'
                yield item
