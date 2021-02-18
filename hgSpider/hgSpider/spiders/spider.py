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
        # item['content'] = re.sub(r'\n|\n\s', '', item["total"][11:])
        # print(item["content"])
        item['open_date'] = item['open_date_ori'][0:10]
        item["area_code"] = '230400'
        item["url_id"]= '306'
        item["crawl_time"]= datetime.datetime.now()

        # item["clerk"] = response.xpath("//div[@class='detail_list_img'][1]//text()").extract()


        item['content'] = "案由：" + re.sub(r'\n|\n\s', '', item["total"][4]) + \
                          ";开庭时间：" + re.sub(r'\n|\n\s', '', item["total"][7]) + \
                          ";开庭地点：" + re.sub(r'\n|\n\s', '', item["total"][10]) + \
                          ";基本案情：" + re.sub(r'\n|\s', '', item["total"][13])

        # print('*'*10)

        member=[re.sub(r'\n|\s','',itemb) for itemb in item["member"]]
        item["trial_member"]=[itema for itema in member if itema !=""]
        accuser='原告(.*?)诉|与被告.*?'
        # accuser1='原告.*?诉|与被告(.*?)(?!item["reson"]).)*'
        if "原告" in item["title"]:
            item["accuser"]=re.findall(accuser,item["title"])
            # item["defendant"]=re.findall(accuser1,item["title"])
            # print(item["defendant"])



        content1='.*?案情介绍(.*?)'
        # item["content"]=re.findall(content1,content)

        # f=(";".join(e))
        yield item













    # def parse_k(self, response):
    #     navi_list = response.xpath("//div[@class='page_navi']/*").extract()
    #     print(navi_list)
    #     url = "http://tv.hljcourt.gov.cn"
    #     detail_box_list = response.xpath("//div[@class='w-panel-02']/div")
    #     for detail_box in detail_box_list:
    #         d_url_part = detail_box.xpath(".//@href").extract_first()
    #         d_url_full = parse.urljoin(url, d_url_part)
    #         if d_url_part is not None:
    #             yield scrapy.Request(d_url_full, callback=self.parse_detail)
    #
    #     search_url_result = re.search("front.+\d", navi_list[2])
    #     url1 = None
    #     if (search_url_result):
    #         url1 = search_url_result.group()
    #     if url is not None:
    #         next_url = parse.urljoin(url, url1)
    #         print(next_url)
    #         yield scrapy.Request(next_url, callback=self.parse_k())




    # rules = (
    #     # LinkExtractor 链接提取器，提取url地址
    #     # callback 提取出来的url地址的response会交给callback处理（如果不需要处理，可以不写callback）
    #     # follow 提取的url地址的响应是否重新经过rules来提取新url地址（默认False）
    #     Rule(LinkExtractor(allow=r'/web/site0/tab5240/info\d+\.htm'), callback='parse_item'),  # callback不能传递数据。 详情页的url
    #     Rule(LinkExtractor(allow=r'/web/site0/tab5240/module14430/page\d+\.htm'), follow=True),  # 下一页的url
    #     Rule(LinkExtractor(restrict_xpaths=("//div[@id='mainResults']/ul",)), callback="parse_item"),
    # # 也可以通过XPath匹配对应标签中的所有url
    #     # 如果url匹配到上面的规则，就不会继续向下匹配了。
    # )

    #     # 获取下一页
    # next_page_url = self.base_site + response.xpath(
    #     '//table[@class="p-name"]//a[contains(text(),"下一页")]/@href'
    # ).extract()[0]
    #
    # yield scrapy.Request(next_page_url, callback=self.parse)
    # http: // tv.hljcourt.gov.cn /
    #     urlReqs = []
    #     for url in urls_list:
    #         req = Request(url, self.getDetail)
    #         urlReqs.append(req)
    #     return urlReqs
    #
    # def getDetail(self, response):
    #     print
    #     response.url

    # def parse(self, response):
    #     # logging.warning("*" * 100)
    #     div_list=response.xpath("//div[@class='quote']")
    #     for div in div_list:
    #         item= ToscrapyItem()
    #         item["title"]=div.xpath("./span[@class='text']/text()").extract_first()
    #         item["name"]=div.xpath("./span/small[@class='author']/text()").extract_first()
    #         item["detail_url"]=div.xpath("./span/a/@href").extract_first()
    #         detail_url = parse.urljoin(response.url,item["detail_url"])
    #         yield scrapy.Request(detail_url,callback=self.parse_detail,meta={"item":item})
    # #         找到下一页的request对象
    #     next_url=response.xpath("//li[@class='next']/a/@href").extract_first()
    #     if next_url is not None:
    #         next_url=parse.urljoin(response.url,next_url)
    #         yield scrapy.Request(next_url,callback=self.parse)
    #
    # def parse_detail(self,response):
    #     # 处理详情页解析
    #
    #     item =response.meta["item"]
    #
    #     item["born_date"]=response.xpath("//span[@class='author-born-date']/text()").extract_first()
    #     yield item



        # next_url = response.xpath("//div[@class='pageNavi bg-w']/a[text()='下一页']/@href").extract()
        # 第一页添加列表
        # url = "http://tv.hljcourt.gov.cn"
        # urlc=int(re.findall(r'page/(\d+)',response.urlb)[0])
        # c=re.findall(r'')
        # print(urlc)
        # if urlc==1:
        #     print("#"*10)
        #     a=re.findall(r'(.*/page/)\d+', response.urlb)
        #     # a=re.findall(r'共(\d+)页',response.text)
        #     for i in range(2,c + 1):
        #         b=a+str(i)
        #         yield scrapy.Request(b, callback=self.parse_next)
            # if a:
            #     c=int(a[0])
            #     for i in range(2,c + 1):
            #        b=self.b_prefix+str(i)
            #        yield scrapy.Request(b,callback=self.parse)
