# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymysql
import pymongo


class QunaeronePipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]

        # 创建数据库连接
        client = pymongo.MongoClient(host=host, port=port)

        # 指定数据库
        mydb = client[dbname]

        # 存储数据的表名
        self.sheet = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        self.sheet.insert(data)
        return item


class ConditionChangePipeline(object):
    def __init__(self):
        try:
            self.conn = pymysql.Connect(host='localhost', user='root', password='13567651173', database='python',
                                        charset='utf8')
        except Exception as e:
            print("连接数据库出错,错误原因%s" % e)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        # 爬取详情页链接
        params = [item['url']]

        try:
            sql = self.cur.execute(
                'update qnems_detail_url set is_download = 1 where detail_link = %s',
                params)
            print(sql)
            self.conn.commit()
            # self.cur.close()
            # self.conn.close()
            return item
        except Exception as e:
            print("插入数据出错,错误原因%s" % e)
