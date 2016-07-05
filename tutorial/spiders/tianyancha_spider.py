# coding=utf-8
import sys, time
import scrapy
from scrapy.http import Request
from ..items import CompanyItem
import MySQLdb

reload(sys)
sys.setdefaultencoding("utf-8")


# scrapy crawl tianyancha -o items.json


class MySpider(scrapy.Spider):
    name = 'tianyancha'
    allowed_domains = ["tianyancha.com"]
    start_urls = []

    def start_requests(self):
        conn = MySQLdb.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='root',
            db='think',
            charset='utf8'
        )
        cur = conn.cursor()
        cur.execute("select supplier_name from think_supplier_list where qichacha=0 and id>1 and id<3")
        cc = cur.fetchall()

        try:
            url_head = "http://www.tianyancha.com/search/"
            for line in cc:
                self.start_urls.append(url_head + line[0])

            self.start_urls = ['http://www.tianyancha.com/search/%E4%B8%AD%E7%B2%AE%E4%B8%9C%E6%B4%B2%E7%B2%AE%E6%B2%B9%E5%B7%A5%E4%B8%9A(%E5%B9%BF%E5%B7%9E)%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8']
            for count, url in enumerate(self.start_urls):
                cookies = {'TYCID': '21dbce00900b49c59ec6b6f7ca9c4577',
                           'tnet': '113.106.7.228',
                           'token': '2e4e5cd529854121966c09810b664ef1',
                           '_utm': '17bc483bea1847e88c25ec27e7b965e6'}
                yield Request(url, cookies=cookies, callback=self.parse)

        finally:
            cur.close()
            conn.close()

    def parse(self, response):
        output = response.body
        f = open('f.txt', 'a')
        f.write(output)
        f.close()

        href = response.xpath(
            '//*[@id="ng-view"]/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/a/@href').extract()[
                   0]
        # except:
        #     href = ''
        #     print 'href wrong'
        time.sleep(3)

        if href:
            yield Request(href, callback=self.parse_item)

    def parse_item(self, response):

        item = CompanyItem()
        # item['company_name'] = url.split('=')[1]

        item['registration_number'] = response.xpath('//section[1]/div[2]/ul/li[1]/text()').extract()[0]
        item['annual'] = response.xpath('//section[1]/div[1]/ul/li[1]/a/span/text()').extract()[0]
        print item
        yield item
