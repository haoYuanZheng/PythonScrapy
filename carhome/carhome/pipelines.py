# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
from PIL import Image
from io import BytesIO


class CarhomePipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'carimages':
            # print(item['folder_name'], item["img_name"], item["img_url"])

            img_path = os.path.join(r"/雪弗兰", item['folder_name'])
            if not os.path.exists(img_path):
                os.makedirs(img_path)

            # 图片保存到本地
            for img_name, img_url in item['img_url'].items():
                img_save = os.path.join(img_path, img_name)
                res = requests.get(img_url)
                img = Image.open(BytesIO(res.content))
                img.save(img_save)
