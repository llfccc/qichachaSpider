# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    company_name = scrapy.Field()
    artificial_person = scrapy.Field()  # 法人
    href = scrapy.Field()  # 一级链接
    registration_number = scrapy.Field()  # 注册号
    annual = scrapy.Field()  # 最新年检信息
