# -*- coding: utf-8 -*-
import json
import random

import scrapy
import pymysql
import requests
from qunaertwo.items import QunaertwoItem


class GouwuSpider(scrapy.Spider):
    name = 'gouwu'

    headers = {
        'authority': 'm.ctrip.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': 'application/json',
        'x-ctrip-pageid': '10650019636',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36',
        'content-type': 'application/json',
        'origin': 'https://m.ctrip.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://m.ctrip.com/webapp/you/comment/687/49761-sight.html?DistrictName=%E5%A4%A7%E6%85%88%E5%B2%A9%E9%A3%8E%E6%99%AF%E5%8C%BA&from=https%3A%2F%2Fm.ctrip.com%2Fwebapp%2Fyou%2Fgspoi%2Fsight%2F0%2F49761.html%3Fseo%3D0',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': '_abtest_userid=6bac80e8-99f6-4b95-9041-74c651633cc7; _RSG=l7K66kxF3pC_q11cVYmCd9; _RDG=28a3838a6e72dc2bca09b02290ffe3d318; _RGUID=ccc33fbb-8619-41ef-99cc-c227e6041d3f; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; MKT_CKID=1593507303500.ngvx3.mawa; _ga=GA1.2.1016274307.1593507304; GUID=09031103210661382362; hoteluuid=D763CqU3ktO92XM0; _RF1=183.157.5.105; _gid=GA1.2.1637837214.1593693082; MKT_CKID_LMT=1593693082468; HotelCityID=658split%E5%BB%BA%E5%BE%B7splitJiandesplit2020-7-2split2020-07-03split0; Union=OUID=index&AllianceID=4897&SID=155952&SourceID=&createtime=1593697378&Expires=1594302177516; MKT_OrderClick=ASID=4897155952&AID=4897&CSID=155952&OUID=index&CT=1593697377519&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fsid%3D155952%26allianceid%3D4897%26ouid%3Dindex&VAL={"pc_vid":"1593507300709.1alank"}; gad_city=78a2062d1790b42fa1a75f591a7869b2; __zpspc=9.10.1593697377.1593697520.3%232%7Cwww.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; _jzqco=%7C%7C%7C%7C1593693082534%7C1.1049366552.1593507303498.1593697425577.1593697520329.1593697425577.1593697520329.undefined.0.0.38.38; appFloatCnt=32; _bfs=1.19; _bfi=p1%3D10650032348%26p2%3D10650000804%26v1%3D139%26v2%3D137; nfes_isSupportWebP=1; ibu_h5_lang=en; ibu_h5_local=en-us; _pd=%7B%22r%22%3A13%2C%22d%22%3A79%2C%22_d%22%3A66%2C%22p%22%3A79%2C%22_p%22%3A0%2C%22o%22%3A80%2C%22_o%22%3A1%2C%22s%22%3A80%2C%22_s%22%3A0%7D; nfes_isSupportWebP=1; MKT_Pagesource=H5; hoteluuidkeys=hfPYQgEs3e1De9TrAYGcYaSE9YkLeLTEScj8kWFY5cRXtjLzydUjfY3tIctwXaJLBWMYOUx05j7BiSMjqYBzE9XJmoy7tKPtvB3YG8RcsjPly4Y1oKkgvL8Y6AWz7jMBezQikFYZY8YB6rzUE6BwLDx4fYPQjmtjTNWfYkYdYqfYA4iG0iZAi30IMYnHYD9j3NWO6wpBJzfi67JtzybYXpRMZJpTvfMilbwH4vD4jsMEUXED5wsFR7Lil4Y1Y90JpFy58wLsitSETMJsFy6OiQarkGjO9RnlvGAYnnxMgrDnW0YzYngx35eHZygOYlmjmfwSHwAZiatwoYozjpmw4fvZU; hotelhst=1164390341; _bfa=1.1593507300709.1alank.1.1593697146526.1593698476226.17.143.10650019636; _gat=1'
    }

    # 初始化，从数据库获取详情链接
    def __init__(self):
        try:
            self.conn = pymysql.Connect(host='localhost', port=32769, user='root', password='123456', database='python',
                                        charset='utf8')
            cur = self.conn.cursor()
            sql = 'select scenic_id,name from xiecheng_scenic_detail_url where install = 1 limit 1'
            cur.execute(sql)
            self.urls = list(cur.fetchall())
        except Exception as e:
            print("连接数据库出错,错误原因%s" % e)

    # 直接爬取详情页
    def start_requests(self):
        for url in self.urls:
            item = QunaertwoItem()
            item['scenic_id'] = url[0]
            item['name'] = url[1]
            yield scrapy.Request(url="https://piao.ctrip.com/dest/t" + url[0] + ".html", callback=self.step_one,
                                 headers=self.headers,
                                 meta={'item': item})

    # 详情页部分内容
    def step_one(self, response):
        item = response.meta['item']
        comment = []
        url = "https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList?_fxpcqlniredt=09031103210661382362&__gw_appid=99999999&__gw_ver=1.0&__gw_from=10650019636&__gw_platform=H5"
        payload = "{\n    \"arg\": {\n        \"resourceId\": 49761,\n        \"resourceType\": 11,\n        \"pageIndex\": 2,\n        \"pageSize\": 10,\n        \"sortType\": 3,\n        \"commentTagId\": 0,\n        \"collapseType\": 1,\n        \"channelType\": 7,\n        \"videoImageSize\": \"700_392\",\n        \"starType\": 0\n    },\n    \"head\": {\n        \"cid\": \"09031103210661382362\",\n        \"ctok\": \"\",\n        \"cver\": \"1.0\",\n        \"lang\": \"01\",\n        \"sid\": \"8888\",\n        \"syscode\": \"09\",\n        \"auth\": null,\n        \"extension\": [\n            {\n                \"name\": \"protocal\",\n                \"value\": \"https\"\n            }\n        ]\n    },\n    \"contentType\": \"json\"\n}"
        payload_dict = json.loads(payload)
        for pageIndex in range(51):
            if pageIndex == 0:
                pass
            else:
                arg = payload_dict['arg']
                arg['pageSize'] = pageIndex
                arg['resourceId'] = int(item['scenic_id'])
                payload_dict['arg'] = arg
                response = requests.request("POST", url, headers=self.headers,
                                            data=json.dumps(payload_dict, sort_keys=True, indent=4))
                response_dict = json.loads(response.text.encode('utf8'))
                result = response_dict['result']
                comment_list = result['items']
                if comment_list is not None and len(comment_list):
                    for com in comment_list:
                        comment.append(com)
                else:
                    break
        item['comment'] = comment
        yield item
