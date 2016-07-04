# coding=utf-8
import sys, time
reload(sys)
sys.setdefaultencoding("utf-8")

import scrapy
from scrapy.http import Request
from ..items import QichachaItem


class MySpider(scrapy.Spider):
    name = 'qichacha'
    allowed_domains = ["qichacha.com"]
    start_urls = []

    def start_requests(self):
        file_object = open('company_name.txt', 'r')
        file_content = file_object.readlines()

        try:
            url_head = "http://www.qichacha.com/search?key="
            for line in file_content:

                self.start_urls.append(url_head + line)

            for url in self.start_urls:
                item = QichachaItem()
                item['company_name'] = url.split('=')[1]
                yield Request(url, meta={'item': item})

        finally:
            file_object.close()

    def parse(self, response):
        # try:
            item = response.meta['item']
            print item['company_name'].decode()
            try:
                href = response.xpath('//*[@id="searchlist"]/table/tbody/tr[1]/td[2]/span/a/@href').extract()[0].split('.')[
                           0][9:]
            except:
                href=''
                print 'wrong'
            time.sleep(3)
            cookies = {'gr_user_id': '753e88a4-467d-47ab-8c45-2ef617834e0a',
                       'PHPSESSID': 'qk5ctu7ahha5s61bntip7vlv56',
                       'SERVERID': 'b7e4e7feacd29b9704e39cfdfe62aefc|1467599111|1467599097',
                       'gr_session_id_9c1eb7420511f8b2': 'eb7be3cd-731c-4be5-8542-774f5d5a619f'}
            href_base = 'http://www.qichacha.com/company_getinfos?unique=' + href + '&companyname=%E6%9D%AD%E5%B7%9E%E6%B5%99%E5%9C%B0%E9%9D%9E%E9%87%91%E5%B1%9E%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&tab=base'
            href_report = 'http://www.qichacha.com/company_getinfos?unique=' + href + '&companyname=%E6%9D%AD%E5%B7%9E%E6%B5%99%E5%9C%B0%E9%9D%9E%E9%87%91%E5%B1%9E%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&tab=report'


            if href:
                yield Request(href_base, cookies=cookies, callback=self.parse_item,
                              meta={'item': item, 'category': 'base'})
                time.sleep(3)
                yield Request(href_report, cookies=cookies, callback=self.parse_item,
                              meta={'item': item, 'category': 'report'})
        # except:
        #     pass

    def parse_item(self, response):

        # item['company_name'] = response.xpath('//*[@id="company-top"]/div/div[1]/span[2]/span[1]/text()').extract()[0]
        output = response.body
        item = response.meta['item']
        category = response.meta['category']

        if category == 'base':
            item['registration_number'] = response.xpath('//section[1]/div[2]/ul/li[1]/text()').extract()[0]
        if category == 'report':
            item['annual'] = response.xpath('//section[1]/div[1]/ul/li[1]/a/span/text()').extract()[0]

        yield item
        # f = open('f.txt', 'a')
        # f.write(output)
        # f.close()
        # item['artificial_person'] = response.xpath('//*[@id="searchlist"]/ul/a[1]/span[2]/small[1]/text()[2]').extract()[0]
        # item['year'] = response.xpath('//*[@id="searchlist"]/ul/a[1]/span[2]/small[1]/text()[3]').extract()[0]
