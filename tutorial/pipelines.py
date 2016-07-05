# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


class TutorialPipeline(object):
    def process_item(self, item, spider):
        print ('start')
        try:
            if item['annual'] and item['registration_number']:
                print "pipe", item
                conn = MySQLdb.connect(
                    host='127.0.0.1',
                    port=3306,
                    user='root',
                    passwd='root',
                    db='think',
                    charset='utf8'
                )
                cur = conn.cursor()
                cur.execute("update think_supplier_list annual='%s', qichacha=1  where supplier_name='%s'"
                            ,(item['annual'], item['supplier_name']))
                cur.commit()
                cur.close()
                conn.close()
                return item
        except:
            pass
