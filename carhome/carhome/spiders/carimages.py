# -*- coding: utf-8 -*-
import scrapy
import re
import json
from carhome.items import CarhomeItem


class CarimagesSpider(scrapy.Spider):
    name = 'carimages'
    headurl = "http://panovr.autoimg.cn/pano/"

    def start_requests(self):
        url = 'https://pano.autohome.com.cn/car/ext/30277#pvareaid=2042305'
        yield scrapy.Request(url=url, callback=self.step_one)

    def step_one(self, response):
        res = re.findall(r"<script.*?>.*?</script>", response.text, re.I | re.S | re.M)[1]
        data = re.findall('\[.*?\]', res)
        urls = []
        for order in range(40):
            if order == 0:
                pass
            else:
                current = json.loads(data[order])
                for cur in current:
                    urls.append(self.headurl+cur.get("Url"))

        img_url_dict = {}
        index = 0
        for url in urls:
            index += 1
            img_name = str(index) + ".png"
            img_url = url
            img_url_dict[img_name] = img_url

            item = CarhomeItem()
            item['img_url'] = img_url_dict
            item['folder_name'] = "blue"
            item['img_name'] = img_name
            yield item
