# coding=utf-8
import sys, time

reload(sys)
sys.setdefaultencoding("utf-8")

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
        href1 = 'http://www.qichacha.com/company_getinfos?unique=' + href + '&companyname=%E6%9D%AD%E5%B7%9E%E6%B5%99%E5%9C%B0%E9%9D%9E%E9%87%91%E5%B1%9E%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&tab=base'
        print (href1)
        time.sleep(3)

        if href:
            yield Request(href1, cookies={
                'gr_user_id': '753e88a4-467d-47ab-8c45-2ef617834e0a', 'PHPSESSID': 'bpovvumqj3r1k2fted0llk24i4',
                ' gr_session_id_9c1eb7420511f8b2': '7149af68-332b-486e-bb14-878dc10ca7ee',
                'CNZZDATA1254842228': '861751941-1464243264-null%7C1466143797',
                'CNZZDATA1256793290': '1859997897-1464246286-https%253A%252F%252Fwww.baidu.com%252F%7C1466146192',
                'SERVERID': '4ec4b3b70ba1eea2ca3e9ee7bf352bba|1466146755|1466123828'}
                          , callback=self.parse_item)

    def parse_item(self, response):
        item = DmozItem()
        # item['company_name'] = response.xpath('//*[@id="company-top"]/div/div[1]/span[2]/span[1]/text()').extract()[0]
        # item['registration_number'] = response.xpath('//section[1]/div[2]/ul/li[1]/text()').extract()[0]
        print(response.body)
        # item['artificial_person'] = response.xpath('//*[@id="searchlist"]/ul/a[1]/span[2]/small[1]/text()[2]').extract()[0]
        # item['year'] = response.xpath('//*[@id="searchlist"]/ul/a[1]/span[2]/small[1]/text()[3]').extract()[0]
        #
        # yield item
