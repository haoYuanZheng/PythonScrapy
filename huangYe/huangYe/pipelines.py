# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import json


class HuangyePipeline(object):
    def __init__(self):
        try:
            self.conn = pymysql.Connect(host='localhost', user='root', password='13567651173', database='python',
                                        charset='utf8')
        except Exception as e:
            print("连接数据库出错,错误原因%s" % e)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        params = [item['company_name'], item['company_introduction'], item['contact_person'], item['contact_tel'],
                  item['company_address']]
        try:
            sql = self.cur.execute(
                'insert into python_test(company_name, company_introduction, contact_person, contact_tel, company_address)values (%s,%s,%s,%s,%s)',
                params)
            print(sql)
            self.conn.commit()
        except Exception as e:
            print("插入数据出错,错误原因%s" % e)

    def close_spider(self, spider):
        with open('page_index.json', 'w') as f:
            content = json.dumps(spider.page_index_list)
            f.write(content)

        # f=open('page_index.json','w')
        # content = json.dumps(spider.page_index_list)
        # f.write(content)
        # f.close()



        self.cur.close()
        self.conn.close()
