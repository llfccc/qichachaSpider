# coding=utf-8
import sys, time
#
# reload(sys)
# sys.setdefaultencoding("utf-8")

import scrapy
from scrapy.http import Request
from ..items import DmozItem


class MySpider(scrapy.Spider):
    name = 'qichacha'
    allowed_domains = ["qichacha.com"]
    start_urls = []

    def start_requests(self):
        file_object = open('company_name.txt', 'r')

        try:
            url_head = "http://www.qichacha.com/search?key="
            for line in file_object:
                self.start_urls.append(url_head + line)

            # for url in self.start_urls:
            #     yield self.make_requests_from_url(url)

            for url in self.start_urls:
                yield Request(url)

        finally:
            file_object.close()
            # years_object.close()

    def parse(self, response):
        href = response.xpath('//*[@id="searchlist"]/ul/a[1]/@href').extract()[0].split('.')[0][9:]
        time.sleep(3)
        cookies = {'gr_user_id': '753e88a4-467d-47ab-8c45-2ef617834e0a',
                   'PHPSESSID': '1c0c8jh2i8ktljhqn3upi01mv4',
                   'SERVERID': 'b7e4e7feacd29b9704e39cfdfe62aefc|1466989946|1466987928',
                   'gr_session_id_9c1eb7420511f8b2': '0b1de50e-09f0-40bb-ae92-dca93f8e83e9'}
        href_base = 'http://www.qichacha.com/company_getinfos?unique=' + href + '&companyname=%E6%9D%AD%E5%B7%9E%E6%B5%99%E5%9C%B0%E9%9D%9E%E9%87%91%E5%B1%9E%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&tab=base'
        href_report = 'http://www.qichacha.com/company_getinfos?unique=' + href + '&companyname=%E6%9D%AD%E5%B7%9E%E6%B5%99%E5%9C%B0%E9%9D%9E%E9%87%91%E5%B1%9E%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&tab=report'
        item = DmozItem()
        if href:
            yield Request(href_base, cookies=cookies, callback=self.parse_item, meta={'item': item, 'category': 'base'})
            time.sleep(3)
            yield Request(href_report, cookies=cookies, callback=self.parse_item, meta={'item': item, 'category': 'report'})
        print (item)

    def parse_item(self, response):
        item = response.meta['item']
        category = response.meta['category']
        if category == 'base':
            item['registration_number'] = response.xpath('//section[1]/div[2]/ul/li[1]/text()').extract()[0]
            yield item
        if category == 'report':
            item['year'] = response.xpath('//section[1]/div[1]/ul[1]/li[1]/a/span/text()').extract()[0]



        #
        # output = response.body
        # f = open('f.txt', 'a')
        # f.write(output)
        # f.close()