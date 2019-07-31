# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import json


class XiechengPipeline(object):
    def __init__(self):
        try:
            self.conn = pymysql.Connect(host='localhost', user='root', password='13567651173', database='python',
                                        charset='utf8')
        except Exception as e:
            print("连接数据库出错,错误原因%s" % e)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        params = [item['detail_link'], item['area']]
        try:
            sql = self.cur.execute(
                'insert into xqgw_detail_url(detail_link,area)values (%s,%s)',
                params)
            print(sql)
            self.conn.commit()
        except Exception as e:
            print("插入数据出错,错误原因%s" % e)

    def close_spider(self, spider):
        with open('page_success.json', 'w') as f:
            content = json.dumps(spider.page_success_log)
            f.write(content)
        self.cur.close()
        self.conn.close()
