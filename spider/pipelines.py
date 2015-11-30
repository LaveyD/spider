# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from scrapy.selector import Selector
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
import MySQLdb
import MySQLdb.cursors


class JdspiderPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host='10.222.49.26',
                                            db='jdspider',
                                            user='root',
                                            passwd='123456',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8',
                                            use_unicode=False)
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        tx.execute("select * from JD_ITEMS where ITEM_PRODUCTION_ID = %s and ITEM_DATE = %s",
                   (item['productId'], item['date']))
        result = tx.fetchone()
        log.msg(result, level=log.DEBUG)
        #print result
        if result:
            log.msg("Item already stored in db:%s" % item, level=log.DEBUG)
        else:
            print '========================processing============================='
            log.msg("========================processing=============================", level=log.INFO)
            brand = category = shopname = production_name = None
            if item.get('brand'):
                brand = item['brand']
            if item.get('category'):
                category = item['category']
            if item.get('shopname'):
                shopname = item['shopname']
            if item.get('productionName'):
                production_name = item['productionName']

            tx.execute(
                "insert into JD_ITEMS (ITEM_BRAND, ITEM_NAME, ITEM_CATEGORY,ITEM_SHOP_NAME, ITEM_PRODUCTION_NAME, " +
                "ITEM_URL, ITEM_PRODUCTION_ID, ITEM_PRICE, ITEM_COMMENT_COUNT, ITEM_AVERAGE_SCORE, " +
                "ITEM_SHOW_EVALUATION_COUNT, ITEM_GOOD_EVALUATION_COUNT, ITEM_GOOD_EVALUATION_RATE, " +
                "ITEM_GENERAL_EVALUATION_COUNT, ITEM_GENERAL_EVALUATION_RATE, ITEM_POOR_EVALUATION_COUNT," +
                " ITEM_POOR_EVALUATION_RATE, ITEM_DATE) " +
                "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (brand, item['name'], category, shopname, production_name, item['url'],
                 item['productId'], item['price'], item['commentCount'], item['averageScore'], item['showCount'],
                 item['goodCount'], item['goodRate'], item['generalCount'], item['generalRate'], item['poorCount'],
                 item['poorRate'], item['date']))
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)
            tx.execute("select * from JD_ITEMS where ITEM_PRODUCTION_ID = %s and ITEM_DATE = %s",
                   (item['productId'], item['date']))
            saved_item = tx.fetchone()
            log.msg(saved_item, level=log.INFO)


    def handle_error(self, e):
        log.err(e)

