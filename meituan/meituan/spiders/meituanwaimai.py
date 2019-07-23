# -*- coding: utf-8 -*-
import scrapy
import pymysql
import random
from meituan.items import MeituanItem


class MeituanwaimaiSpider(scrapy.Spider):
    name = 'meituanwaimai'
    page_success_log = []

    headerOne = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        'Connection': "keep-alive",
        'Cookie': "mta=174300829.1563262088691.1563262749966.1563264562957.5; JSESSIONID=1gnrh66al6gwtm8xsj013b1ef; IJSESSIONID=1gnrh66al6gwtm8xsj013b1ef; iuuid=2BB206A9EB899F3AE8FBE47AB9BE651BA4DAC1B930970BA4B5708CB8C6002742; ci=50; cityname=%E6%9D%AD%E5%B7%9E; a2h=4; _lxsdk_cuid=16bf9ae715bc8-0f152239c20a638-4a5a67-13c680-16bf9ae715bc8; _lxsdk_s=16bf9ae715c-a4-7b4-626%7C%7C16; _lxsdk=2BB206A9EB899F3AE8FBE47AB9BE651BA4DAC1B930970BA4B5708CB8C6002742; i_extend=C189913015384320739764905118182476349850_b1_c0_e25647423475505834134H__a; webp=1; latlng=30.253193,120.212887,1563264563555; __utma=74597006.502873269.1563262088.1563262088.1563262088.1; __utmb=74597006.22.9.1563264567874; __utmc=74597006; __utmz=74597006.1563262088.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); uuid=67942778-b802-4a50-b632-bdeb65137e81; _hc.v=4b77e746-d549-0d33-2bc5-3cdfa0f96232.1563264558; webloc_geo=30.253193%2C120.212887%2Cwgs84%2C-1",
        'Upgrade-Insecure-Requests': "1",
        'cache-control': "no-cache",
    }

    headerTwo = {
        'Connection': "keep-alive",
        'Cache-Control': "max-age=0",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cookie': "__mta=147626888.1563254982505.1563329489622.1563332139099.30; __mta=147626888.1563254982505.1563267232927.1563267262223.9; _lxsdk_cuid=16be4f5cc8cc8-0240436930d281-62370b78-13c680-16be4f5cc8cc8; rvct=50; _hc.v=9f4ef3a5-7b4e-5d8d-1ae8-380e04061e58.1562914478; uuid=e00f0425cab54d22b4ff.1563153716.1.0.0; lat=30.23654; lng=120.17052; IJSESSIONID=a92ub2v57eka1opf0wmfk9liu; iuuid=0A9C23D62E3B408D39FB09C8E6627022FA06267DFF176982D7178DCED0BC0006; _lx_utm=utm_campaign%3Dm.baidu%26utm_medium%3Dorganic%26utm_source%3Dm.baidu%26utm_content%3D100005%26utm_term%3D; _lxsdk=0A9C23D62E3B408D39FB09C8E6627022FA06267DFF176982D7178DCED0BC0006; __utmc=74597006; __utmz=74597006.1563254963.1.1.utmcsr=m.baidu|utmccn=m.baidu|utmcmd=organic|utmcct=100005; ci3=1; client-id=74fc7c3f-2c44-4823-a182-e268752a51db; logan_custom_report=; ci=50; cityname=%E6%9D%AD%E5%B7%9E; a2h=4; meishi_ci=50; __utma=74597006.2126041018.1563254963.1563327861.1563332131.9; latlng=30.287467,120.153589,1563332131048; __utmb=74597006.2.9.1563332131; i_extend=C189913015384320739764905118182476349850_b1_c0_e170898508498592428444H__a; logan_session_token=oc23wu2wwifg6s4gg7ho; _lxsdk_s=16bfddb36d1-4c1-df7-13e%7C%7C4",
        'cache-control': "no-cache",
    }

    headerThree = {
        'Connection': "keep-alive",
        'Cache-Control': "max-age=0",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache",
    }

    suffixTwo = '&cevent=imt%2Fdeal%2Flist%2Flist-item'

    # 初始化，从数据库获取详情链接
    def __init__(self):
        try:
            self.conn = pymysql.Connect(host='localhost', user='root', password='13567651173', database='python',
                                        charset='utf8')
            cur = self.conn.cursor()
            sql = 'select url from detail_url'
            cur.execute(sql)
            self.urls = list(cur.fetchall())
            random.shuffle(self.urls)
        except Exception as e:
            print("连接数据库出错,错误原因%s" % e)

    # 直接爬取详情页
    def start_requests(self):
        for url in self.urls:
            print("爬取链接::::::::"+url[0])
            yield scrapy.Request(url=url[0], callback=self.third, headers=self.headerThree)

    # 从列表开始爬取
    # def start_requests(self):
    #     url = 'http://i.meituan.com/hangzhou/all/?cateType=deal&stid_b=4'
    #     yield scrapy.Request(url=url, callback=self.third, headers=self.headerOne)

    def second(self, response):
        sign = 0
        thirdLinks = response.xpath('//div[@id="deals"]/dl/dd/dl/dd/a/@href').extract()
        current_page = response.xpath('//*[@id="deals"]/dl/dd[2]/div/span/text()').extract_first()
        self.page_success_log.append(current_page)
        for tl in thirdLinks:
            sign += 1
            siffixOne = "?stid=" + response.xpath('//div[@id="deals"]/dl/dd/dl/dd[$sign]/a/@data-stid',
                                                  sign=sign).extract_first()
            tl = ("http:" + tl + siffixOne + self.suffixTwo)
            # 爬取详情页链接
            # item = MeituanItem()
            # item['url'] = tl
            # yield item
            yield scrapy.Request(url=tl, callback=self.third, headers=self.headerTwo)
        nextBtn = response.xpath('//*[@id="deals"]/dl/dd[2]/div/a[2]/@href').extract_first()
        if nextBtn is not None and current_page != 1:
            nextBtn = "http:" + nextBtn
            yield scrapy.Request(url=nextBtn, callback=self.second, headers=self.headerOne)

    def third(self, response):
        item = MeituanItem()
        item['meal_name'] = response.xpath('//*[@id="app"]/div/div[1]/div[2]/div/a/div/h1/text()').extract_first()
        item['meal_type'] = response.xpath('//*[@id="app"]/div/div[1]/div[2]/div/a/div/span/text()').extract_first()

        realPrice = response.xpath('//*[@id="top-box"]/div/div/strong/text()').extract_first()
        if realPrice is not None:
            realPrice += "元;"
            realPrice += "".join(response.xpath('//*[@id="top-box"]/div/div/span[2]/text()').extract())
        item['price'] = realPrice

        items = response.xpath('//*[@id="app"]/div/div[1]/div[2]/div/div[2]/div[3]/ul/li/span/text()').extract()
        support_items = []
        for e in items:
            support_items.append(e)
        item['support_items'] = ",".join(support_items)

        labels = response.xpath('//*[@id="app"]/div/div[1]/div[2]/div/div[3]/div[2]/a/span/text()').extract()
        label = []
        for l in labels:
            label.append(l)
        item['label'] = "/".join(label)

        company = response.xpath(
            '//*[@id="app"]/div/div[1]/div[2]/div/div[4]/div[2]/div/div[1]/a/h5/text()').extract_first()
        if company is not None:
            company += ':'
            company += response.xpath(
                '//*[@id="app"]/div/div[1]/div[2]/div/div[4]/div[2]/div/div[1]/a/div[1]/text()').extract_first()
        item['company'] = company
        item['comment'] = "".join(
            response.xpath('//*[@id="app"]/div/div[1]/div[2]/div/div[5]/div[2]/div/div[2]/ul/li/text()').extract())
        yield item
