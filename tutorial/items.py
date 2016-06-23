# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DmozItem(scrapy.Item):
    company_name = scrapy.Field()
    artificial_person = scrapy.Field()
    year = scrapy.Field()
    href = scrapy.Field()
    registration_number = scrapy.Field()
    annual = scrapy.Field()


