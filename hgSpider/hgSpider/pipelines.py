# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# -*- coding: utf-8 -*-
import os
import csv
# useful for handling different item types with a single interface
import re
import pymysql
from itemadapter import ItemAdapter
from hgSpider.items import HgspiderItem
import MySQLdb

class HgspiderPipeline:
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root', password='123456', db='spiderpython_dev', port=3306,charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 新的url进行存储
        insert_sql = """
                       insert into t_sp_courtnotice(court,forum,open_date,open_date_ori,reason,trial_member,content,area_name,area_code,crawl_time,url,url_id,accuser)
                       VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)
                   """
        self.cursor.execute(insert_sql,
                            (item['court'],item['forum'],item['open_date'],item['open_date_ori'],item['reason'],item['trial_member'],
                             item['content'],item['area_name'],item['area_code'],item['crawl_time'],item['url'],item['url_id'],item['accuser']))
     
        self.conn.commit()
        return item
   
