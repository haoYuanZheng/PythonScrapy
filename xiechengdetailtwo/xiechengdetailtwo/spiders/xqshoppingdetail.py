# -*- coding: utf-8 -*-
import scrapy
import pymysql
import re
import json
import requests
from xiechengdetailtwo.items import XiechengdetailtwoItem
from lxml import etree


class XqshoppingdetailSpider(scrapy.Spider):
    name = 'xqshoppingdetail'

    headers = {
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
            sql = 'select detail_link,area from xqgw_url_single where is_download = 0 limit 5'
            cur.execute(sql)
            self.urls = list(cur.fetchall())
            # random.shuffle(self.urls)
        except Exception as e:
            print("连接数据库出错,错误原因%s" % e)

    # 直接爬取详情页
    def start_requests(self):
        for url in self.urls:
            print("爬取链接::::::::" + url[0])
            item = XiechengdetailtwoItem()
            item['url'] = url[0]
            item['area'] = url[1]
            yield scrapy.Request(url=url[0], callback=self.step_one, headers=self.headers, meta={'item': item})

    # 第一个详情页
    def step_one(self, response):
        item = response.meta['item']
        name = response.xpath('/html/body/div[2]/div[2]/div/div[1]/h1/a/text()').extract_first()
        if name is not None:
            item['name'] = name
        address = response.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li/span[2]/text()').extract_first()
        if address is not None:
            address = address.replace("\r", "").replace(" ", "").replace("\n", "").replace("|", "")
        item['address'] = address
        introduce = response.xpath(
            '/html/body/div[3]/div/div[1]/div[3]/div[1]/div[1]/div/div/text()').extract_first()
        if introduce is not None:
            introduce = introduce.replace("\r", "").replace(" ", "").replace("\n", "").replace("|", "")
        item['introduce'] = introduce
        openTime = response.xpath('/html/body/div[3]/div/div[2]/div[1]/dl/dd/text()').extract_first()
        if openTime is not None:
            item['open_time'] = openTime
        one = response.xpath('/html/body/div[3]/div/div[1]/div[4]/div[1]/div[2]/dl/dt/span[2]/text()').extract_first()
        two = response.xpath(
            '/html/body/div[3]/div/div[1]/div[4]/div[1]/div[2]/dl/dd[1]/span[3]/text()').extract_first()
        three = response.xpath(
            '/html/body/div[3]/div/div[1]/div[4]/div[1]/div[2]/dl/dd[2]/span[3]/text()').extract_first()
        four = response.xpath(
            '/html/body/div[3]/div/div[1]/div[4]/div[1]/div[2]/dl/dd[3]/span[3]/text()').extract_first()
        if one is not None and two is not None and three is not None and four is not None:
            item['score'] = "总分:" + one + "," + "商品:" + two + "," + "环境:" + three + "," + "服务:" + four

        # post请求所需要的poid和附加数据
        poiID = response.xpath('//*[@id="dianPing"]/span/a/@data-id').extract_first()
        # 评论总页数
        pageCount = response.xpath(
            '//*[@id="sightcommentbox"]/div[@class="ttd_pager cf"]/div/span/b/text()').extract_first()
        # 防止评论不足10条，获取不到页数
        if pageCount is None:
            pageCount = 1
        # 评论总数
        pageSum = int(response.xpath('//*[@id="comment"]/div/h2/span/span/text()').extract_first())
        currentSum = 0
        # 所有评论集合
        comments = []
        for pageNo in range(int(pageCount) + 1):
            if pageNo == 0:
                continue
            else:
                postData = {'poiID': str(poiID), 'star': '0', 'order': '3', 'tourist': '0', 'pagenow': str(pageNo)}
                url = "https://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView"
                # 调用post请求获取当前页评论数据
                callBack = requests.request("POST", url, data="", headers=self.headers, params=postData)
                html = etree.HTML(callBack.text)
                for index in range(10):
                    currentSum = currentSum + 1
                    if currentSum < pageSum:
                        current = {}
                        username = html.xpath('//*[@class="comment_ctrip"]//div[@class="userimg"]/span/a/text()')[
                            index]
                        rank = html.xpath('//*[@class="comment_ctrip"]//ul/li[1]/span[1]/span/span/@style')[index]
                        commentDetail = html.xpath('//*[@class="comment_ctrip"]//ul/li[2]/span/text()')[index]
                        imageUrl = html.xpath(
                            '//*[@class="comment_ctrip"]//div[@class="comment_single"][$index]/ul/li[3]/a/@href',
                            index=1)
                        if username is not None:
                            current['username'] = username
                        else:
                            continue
                        if rank is not None:
                            current['rank'] = rank.replace(" ", "").replace("\r\n", "").replace("&emsp",
                                                                                                "").replace(
                                "&nbsp", "")
                        if commentDetail is not None:
                            current['commentDetail'] = commentDetail.replace("\r", "").replace(" ", "").replace(
                                "\n",
                                "").replace(
                                "|", "")
                        if imageUrl is not None:
                            current['imageUrl'] = imageUrl
                        comments.append(current)
                    else:
                        break

        # item中放入所有评论
        item['comment'] = comments

        pageTwo = response.xpath('//*[@id="jieshao"]/div/ul/li[2]/h2/a/@href').extract_first()
        if pageTwo is not None:
            yield scrapy.Request(url=self.nextPageHead + pageTwo, callback=self.step_two, meta={'item': item},
                                 headers=self.headers)
        else:
            pass

    # 第二个tab页
    def step_two(self, response):
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
                                     headers=self.headers)
            else:
                yield item

    # 团购tab页
    def step_three(self, response):
        item = response.meta['item']
        nearbyGroupBuy = response.xpath('/html/body/div[3]/div/div[1]/div[3]/ul/li/dl/dt/text()').extract()
        if nearbyGroupBuy is not None:
            nearbyGroupBuy = "|".join(nearbyGroupBuy).replace(" ", "").replace("\r\n", "")
            item['nearby_group_buy'] = nearbyGroupBuy
        yield item
