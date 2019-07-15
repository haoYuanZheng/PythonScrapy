# -*- coding: utf-8 -*-
import scrapy


# from huangYe.items import HuangyeItem


class Huangye88Spider(scrapy.Spider):
    name = 'huangYe88'

    # allowed_domains = ['huangye88.com']
    # start_urls = ['http://huangye88.com/']
    headers = {
        'Connection': "keep-alive",
        'Cache-Control': "max-age=0",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3833.0 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cookie': "Hm_lvt_c8184fd80a083199b0e82cc431ab6740=1562670073,1562726650; Hm_lpvt_c8184fd80a083199b0e82cc431ab6740=1562744611",
        'cache-control': "no-cache",
        # 'Postman-Token': "dc6ed178-107c-4dfc-b098-51a5c361d78d"
    }
    page_index_list = []

    def start_requests(self):
        url = 'http://b2b.huangye88.com/shanghai/'
        yield scrapy.Request(url=url, callback=self.second, headers=self.headers)

    def second(self, response):
        # print(response.text)
        secondLinks = response.xpath('//div[@id="subcatlisting_10"]/ul/li/a/@href').extract()
        for fl in secondLinks:
            yield scrapy.Request(url=fl, callback=self.third, headers=self.headers)

    # 同时需要判断是否要换页
    def third(self, response):
        # print(response.text)
        flag = response.xpath(
            '//div[@class="page_tag Baidu_paging_indicator"]/a[contains(text(),"下一页")]/text()').extract_first()
        thirdLinks = response.xpath('//dt/h4/a/@href').extract()
        current_page = response.xpath('//div[@class="page_tag Baidu_paging_indicator"]/span/text()').extract_first()
        self.page_index_list.append(current_page)
        for tl in thirdLinks:
            tl = tl + "company_detail.html"
            yield scrapy.Request(url=tl, callback=self.fourth, headers=self.headers)
        if flag == '下一页':
            nextUrl = response.xpath(
                '//div[@class="page_tag Baidu_paging_indicator"]/a[contains(text(),"下一页")]/@href').extract_first()
            yield scrapy.Request(url=nextUrl, callback=self.third, headers=self.headers)

    def fourth(self, response):
        # print(response.text)
        item = HuangyeItem()
        item['company_name'] = response.xpath('//div[@class="data"]/p/text()').extract_first()
        item['company_introduction'] = "".join(
            response.xpath('//div[@class="r-content"]/p[@class="txt"]//text()').extract())
        item['contact_person'] = response.xpath('//div[@class="l-content"]/ul/li[1]/a/text()').extract_first()
        item['contact_tel'] = response.xpath('//div[@class="l-content"]/ul/li[4]/text()').extract_first()
        info = response.xpath('//div[@class="data"]/ul[@class="con-txt"]/li')
        base_info = []
        for i in info:
            base_info.append("".join(i.xpath('.//text()').extract()))
        item['company_address'] = ",".join(base_info)
        yield item
