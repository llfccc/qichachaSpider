# coding=utf-8
import sys, time
import scrapy
import MySQLdb
from scrapy.http import Request
from ..items import CompanyItem

reload(sys)
sys.setdefaultencoding("utf-8")


# 运行命令 ####         scrapy crawl qichacha -o items.json


class MySpider(scrapy.Spider):
    name = 'qichacha'
    allowed_domains = ["qichacha.com"]
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
        cur.execute("select supplier_name from think_supplier_list where qichacha=0 and id>20 and id<50")
        cc = cur.fetchall()

        try:
            url_head = "http://www.qichacha.com/search?key="
            for line in cc:
                self.start_urls.append(url_head + line[0])

            for count, url in enumerate(self.start_urls):
                item = CompanyItem()
                print ('now name:', url.split('=')[1])
                item['company_name'] = url.split('=')[1]
                yield Request(url, meta={'item': item})
                if count > 3:
                    break

        finally:
            cur.close()
            conn.close()

    def parse(self, response):
        item = response.meta['item']
        print item['company_name'].decode()
        try:
            href = response.xpath('//*[@id="searchlist"]/table/tbody/tr[1]/td[2]/span/a/@href').extract()[0].split('.')[
                       0][9:]
        except:
            href = ''
            print 'href wrong'
        cookies = {'gr_user_id': '753e88a4-467d-47ab-8c45-2ef617834e0a',
                   'PHPSESSID': 'v58ufgpu2h5b19tqnguq8dtj10',
                   'SERVERID': '0359c5bc66f888586d5a134d958bb1be|1467688506|1467688430',
                   'gr_session_id_9c1eb7420511f8b2': 'c5a55c37-e69c-4308-bc49-fe59b4de7b28'}
        href_base = 'http://www.qichacha.com/company_getinfos?unique=' + href + '&companyname=%E6%9D%AD%E5%B7%9E%E6%B5%99%E5%9C%B0%E9%9D%9E%E9%87%91%E5%B1%9E%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&tab=base'
        href_report = 'http://www.qichacha.com/company_getinfos?unique=' + href + '&companyname=%E6%9D%AD%E5%B7%9E%E6%B5%99%E5%9C%B0%E9%9D%9E%E9%87%91%E5%B1%9E%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&tab=report'

        if href:
            yield Request(href_base, cookies=cookies, callback=self.parse_item,
                          meta={'item': item, 'category': 'base'})
            yield Request(href_report, cookies=cookies, callback=self.parse_item,
                          meta={'item': item, 'category': 'report'})

    def parse_item(self, response):
        item = response.meta['item']
        category = response.meta['category']

        if category == 'base':
            item['registration_number'] = response.xpath('//section[1]/div[2]/ul/li[1]/text()').extract()[0]
        if category == 'report':
            item['annual'] = response.xpath('//section[1]/div[1]/ul/li[1]/a/span/text()').extract()[0]
        yield item
