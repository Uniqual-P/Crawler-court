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
        self.conn = MySQLdb.connect(host='106.75.65.54', user='spiderpython_dev', password='spiderpython_dev@0126', db='spiderpython_dev', port=7749,charset="utf8", use_unicode=True)
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
        # elif isinstance(item, NovelDetailItem):
        #     if redis_db.sismember(self.redis_data_dict, item[
        #         "chapter_url"]):  # 取item里的chapter_url和里的字段对比，看是否存在，存在就丢掉这个item。不存在返回item给后面的函数处理set
        #         print(item["chapter_id"], 'has been finished')
        #         raise DropItem("Duplicate item found: %s" % item)
        #     self.cursor.execute(insert_noveldetail_sql, (item["novel_id"], item["chapter_url"], item["chapter_id"],
        #                                                  item["chapter_name"], item["novel_detail"]))
        self.conn.commit()
        return item
    # for court,forum,open_date,open_date_ori,reason,trial_member,content,area_name,area_code,crawl_time,url,url_id in item:
    #
    #     data = {
    #         'court': court.string,
    #         'forum': forum.string,
    #         'open_date': open_date.datetime,
    #         'open_date_ori': open_date_ori.datetime,
    #         'reason': reason.string,
    #         'trial_member': trial_member.string,
    #         'content': content.string,
    #         'area_name': area_name.string,
    #         'area_code': area_code.string,
    #         'crawl_time': crawl_time.datetime,
    #         'url': url.string,
    #         'url_id': url_id.interger,
    #     }
    #     # print(data['orderNumber'],data['orderNumber'],data['orderNumber'])
    #     conn = pymysql.connect(
    #         host='localhost',
    #         port=3306,
    #         user='root',
    #         password='123456',
    #         db='crawler',
    #         charset='utf8'
    #     )
    #     coursor = conn.cursor()
    #     table = 't_sp_courtnotice'
    #     values = ','.join(['%s'] * len(data))
    #
    #     sql = 'insert into {table}(court,forum,open_date,open_date_ori,reason,trial_member,content,area_name,area_code,crawl_time,url,url_id) values({values})'. \
    #         format(table=table, values=values)
    #     try:
    #         if coursor.execute(sql, tuple(data.values())):
    #             print("插入成功")
    #             conn.commit()
    #     except:
    #         print("插入失败")
    #         conn.rollback()
    #     conn.close()
    # def __init__(self):
    #     self.dbpool =  pymysql.connect(host='localhost', user='root', password='123456', db='crawler', port=3306)
    #     print("连接成功")
    #
    #
    # @classmethod
    # def from_settings(cls, settings):
    #     dbpool = MysqlConnectionPool().dbpool()
    #     return cls(dbpool)
    #
    # # pipeline默认调用
    # def process_item(self, item, spider):
    #     query = self.dbpool.runInteraction(self._conditional_insert, item)
    #     query.addErrback(self._handle_error, item, spider)
    #     return item
    #
    # def _handle_error(self, failue, item, spider):
    #     print(failue)
    #
    # def _conditional_insert(self, transction, item):
    #     tt = transction._connection._connection
    #     try:
    #         tt.ping()
    #     except:
    #         self.dbpool.close()
    #         self.dbpool = MysqlConnectionPool().dbpool()
    #
    #     sql = """insert INTO `t_sp_courtnotice`(court,forum,open_date,open_date_ori,reason,trial_member,content,area_name,area_code,crawl_time,url,url_id)
    #         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    #     params = (
    #         item['court'],
    #         item['forum'],
    #         item['open_date'],
    #         item['open_date_ori'],
    #         item['reason'],
    #         item['trial_member'],
    #         item['content'],
    #         item['area_name'],
    #         item['area_code'],
    #         item['crawl_time'],
    #         item['url'],
    #         item['url_id'],
    #     )
    #     transction.execute(sql, params)
    # def open_spider(self, spider):
    #     db = spider.settings.get('MYSQL_DB_NAME', 'crawler')
    #     host = spider.settings.get('MYSQL_HOST', 'localhost')
    #     port = spider.settings.get('MYSQL_PORT', 3306)
    #     user = spider.settings.get('MYSQL_USER', 'root')
    #     passwd = spider.settings.get('MYSQL_PASSWORD', '123456')
    #
    #     self.db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
    #     self.db_cur = self.db_conn.cursor()
    # #
    # # def reConnect(self):
    # #     try:
    # #         self.connection.ping()
    # #     except:
    # #         self.connection()
    # def execute_db(self, sql):
    #     try:
    #         # 检查连接是否断开，如果断开就进行重连
    #         self.conn.ping(reconnect=True)
    #         self.cur.execute(sql)
    #         self.conn.commit()
    #     except Exception as e:
    #         print("操作出现错误：{}".format(e))
    #         self.conn.rollback()
    # # 关闭数据库
    # def close_spider(self, spider):
    #     self.db_conn.commit()
    #     self.db_conn.close()
    #
    # # 对数据进行处理
    # def process_item(self, item, spider):
    #     self.insert_db(item)
    #     return item
    #
    # def insert_db(self, item):
    #     values = (
    #         item['court'],
    #         item['forum'],
    #         item['open_date'],
    #         item['open_date_ori'],
    #         item['reason'],
    #         item['trial_member'],
    #         item['content'],
    #         item['area_name'],
    #         item['area_code'],
    #         item['crawl_time'],
    #         item['url'],
    #         item['url_id'],
    #     )
    #     try:
    #         sql = 'INSERT INTO t_sp_courtnotice VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    #         self.db_cur.execute(sql, values)
    #         self.db_conn.commit()
    #         print("Insert finished")
    #     except:
    #         print("Insert to DB failed")
    #         self.db_conn.commit()
    #         self.db_conn.close()
            # def open_spider(self, spider):
    #     # 连接数据库
    #     settings = get_project_settings()
    #     print('settings: ', settings)
    #     self.connect = pymysql.connect(
    #         host=settings.get('MYSQL_HOST'),
    #         port=settings.get('MYSQL_PORT'),
    #         db=settings.get('MYSQL_DATABASE'),
    #         user=settings.get('MYSQL_USER'),
    #         passwd=settings.get('MYSQL_PASSWORD'),
    #         charset='utf8',
    #         use_unicode=True)
    # def __init__(self):
    #     # 连接MySQL数据库
    #     self.connect = pymysql.connect(host='localhost', user='root', password='123456', db='crawler', port=3306)
    #     self.cursor = self.connect.cursor()
    #
    #
    # def close_spider(self, spider):
    #     self.cursor.close()
    #     self.connect.close()

    # def process_item(self, item, spider):
    #     settings = get_project_settings()
    #     data = dict(item)
    #     # keys = ', '.join(data.keys())
    #     # values = ', '.join(['%s'] * len(data))
    #     values = self.get_values_in_str(item, keys)
    #     sql = 'insert into %s (%s) values (%s)' % (settings.get("TABLE_NAME"), keys, values)
    #     self.cursor.execute(sql)
    #     return item

    # def get_values_in_str(self, item, key_list_str):
    #     key_list = key_list_str.split(", ")
    #     rtn_str = ""
    #     for key in key_list:
    #         if (item[key]) is None:
    #             rtn_str += " '',"
    #         else:
    #             rtn_str += " '" + str(item[key]) + "',"
    #     rtn_str=rtn_str[0:-1]
    #     return rtn_str


    # def process_item(self, item):
    #     self.cursor.execute( (item['court'], item['forum'], item['opern_date'], item['open_date_ori'], item['case_code'],item['case_code_ori'],
    #                                           item['reason'], item['depart'], item['judge'], item['clerk'], item['juryman'], item['trial_member'],item['is_open'],
    #                                           item['accuser'], item['defendant'], item['litigant'], item['result'], item['purpose'], item['is_annul'],item['content'],
    #                                           item['area_name'], item['area_code'], item['crawl_id'], item['crawl_time'], item['url'], item['url_id'],item['text'],
    #                                           item['update_time'], item['excel_name'], item['publish_date'],))
    #     self.connect.commit()
        # return item

    # def close_spider(self, spider):
    #     self.cursor.close()
    #     self.connect.close()

        # if spider.name == "spider":
        #     item['content'] = self.clean_content(item['content'])
        #     item['member'] = self.clean_content(item['member'])
        # # print(item)
        # return item

    # def clean_content(self, content):
    #     return re.sub(r'\n|\s', '', content)
