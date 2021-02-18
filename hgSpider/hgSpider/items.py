# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HgspiderItem(scrapy.Item):
    table = "t_sp_courtnotice"
    urls_list = scrapy.Field()
    urls_next = scrapy.Field()
    detail_url = scrapy.Field()
    next_url = scrapy.Field()
    title = scrapy.Field()
    court = scrapy.Field()
    reason = scrapy.Field()
    urls_detail= scrapy.Field()
    clerk= scrapy.Field()
    member= scrapy.Field()
    detail = scrapy.Field()
    content = scrapy.Field()
    forum = scrapy.Field()
    open_date = scrapy.Field()
    open_date_ori = scrapy.Field()
    case_code = scrapy.Field()
    case_code_ori = scrapy.Field()
    depart = scrapy.Field()
    judge = scrapy.Field()
    juryman = scrapy.Field()
    trial_member = scrapy.Field()
    is_open = scrapy.Field()
    accuser = scrapy.Field()
    defendant = scrapy.Field()
    litigant = scrapy.Field()
    result = scrapy.Field()
    purpose = scrapy.Field()
    is_annul = scrapy.Field()
    area_name = scrapy.Field()
    area_code = scrapy.Field()
    crawl_time = scrapy.Field()
    url = scrapy.Field()
    url_id= scrapy.Field()
    update_time = scrapy.Field()
    text = scrapy.Field()
    excel_name = scrapy.Field()
    publish_date = scrapy.Field()
    total = scrapy.Field()
    a = scrapy.Field()


