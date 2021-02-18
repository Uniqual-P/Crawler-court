import re
from copy import deepcopy
import datetime
from urllib import parse
from urllib.parse import urljoin
import chardet

import scrapy

from hgSpider.items import HgspiderItem
from openpyxl.styles.builtins import total


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['hljcourt.gov.cn']
    start_urls = ['http://tv.hljcourt.gov.cn/index/index/court/196']

    def parse(self, response):
        item = HgspiderItem()
        item["urls_list"] = re.findall(b'<a href="(/video/sort/tid/\d+/court/196)"',response.body)
        url = "http://tv.hljcourt.gov.cn"
        # # url = url.encode('utf-8').decode('utf-8')
        for urllist in item['urls_list']:
            urla = str(url) + str(urllist,'utf-8')
            # urla = urla.encode('utf-8').decode('utf-8')
            yield scrapy.Request(urla, callback=self.parse_next, meta={"item": deepcopy(item)})

    def parse_next(self,response):
        item = HgspiderItem()
        item['urls_detail']=re.findall(b'<a href="(/video/detail/court/196/id/\d+)"',response.body)
        url = "http://tv.hljcourt.gov.cn"
        for urlnext in item['urls_detail']:
            item["url"] = str(url) + str(urlnext,'utf-8')
            # urla = urla.encode('utf-8').decode('utf-8')
            yield scrapy.Request(item["url"], callback=self.parse_detail, meta={"item": deepcopy(item)})

        number_page=int(re.findall(r'共(\d+)页',response.text)[0])
        url_number=re.findall(r'/front/video/sort/tid/\d+/court/',response.text)[0]
        a="196/196/page/page/"
        b="http://tv.hljcourt.gov.cn"
        if number_page>1:
            for i in range (2,number_page+1):
                urlc=str(b)+str(url_number)+str(a)+str(i)
                yield scrapy.Request(urlc,callback=self.parse_next)

    def parse_detail(self,response):
        item = response.meta["item"]
        item["title"] = response.xpath("//div[@class='detail_title']/text()").extract_first()
        item["court"] = response.xpath("//div[@class='detail_title2']/text()").extract_first()[3:]
        print(item["court"])
        item["total"] = response.xpath(".//div[@class='detail_info']//text()").extract()
        item["member"] = response.xpath("//div[@class='detail_list_img']//text()").extract()
        item['area_name'] = '黑龙江省鹤岗市'
        item['reason'] = re.sub(r'\n|\n\s', '', item["total"][4])
        item['open_date_ori'] = re.sub(r'\n|\n\s', '', item["total"][7])
        item['forum'] = re.sub(r'\n|\n\s', '', item["total"][10])

        item['open_date'] = item['open_date_ori'][0:10]
        item["area_code"] = '230400'
        item["url_id"]= '306'
        item["crawl_time"]= datetime.datetime.now()

        item['content'] = "案由：" + re.sub(r'\n|\n\s', '', item["total"][4]) + \
                          ";开庭时间：" + re.sub(r'\n|\n\s', '', item["total"][7]) + \
                          ";开庭地点：" + re.sub(r'\n|\n\s', '', item["total"][10]) + \
                          ";基本案情：" + re.sub(r'\n|\s', '', item["total"][13])

        member=[re.sub(r'\n|\s','',itemb) for itemb in item["member"]]
        item["trial_member"]=[itema for itema in member if itema !=""]
        accuser='原告(.*?)诉|与被告.*?'
        if "原告" in item["title"]:
            item["accuser"]=re.findall(accuser,item["title"])

        content1='.*?案情介绍(.*?)'

        yield item


