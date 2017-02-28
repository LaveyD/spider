#__author__ = 'fuma2'

from pymongo import MongoClient
import datetime
from scrapy.exceptions import DropItem
from scrapy.conf import settings
#from scrapy import log


class MongoPipeline(object):
    MONGODB_SERVER = "localhost"
    MONGODB_PORT = 27017
    MONGODB_DB = "JDITEMS"
    MONGODB_COLLECTION = "JDSPIDERS"
    #connect to mongodb
    def __init__(self):
        print "======================Parameters below========================="
        print self.MONGODB_SERVER, self.MONGODB_PORT, self.MONGODB_DB, self.MONGODB_COLLECTION
        #print settings['MONGODB_SERVER'], settings['MONGODB_PORT'], settings['MONGODB_DB'], settings['MONGODB_COLLECTION']

        try:
            client = MongoClient(self.MONGODB_SERVER, self.MONGODB_PORT)
            self.db = client[self.MONGODB_DB]
            print self.db
        except Exception as e:
            print "ERROR(MongoPipeline):", e
        # connection = pymongo.Connections('localhost', '27017')
        # db = connection['DOUBANMOVIE']
        # self.collection = db['DOUBANMOVIES']
        # connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        # print connection
        # db = connection[settings['MONGODB_DB']]
        #self.collection = db[self.MONGODB_COLLECTION]]

    def process_item(self, item, spider):
        #print 'processing============================='+ datetime.datetime.utcnow()
        #log.msg("========================processing=============================", level=log.INFO)
        brand = category = shopname = production_name = None
        if item.get('brand'):
            brand = item['brand']
        if item.get('category'):
            category = item['category']
        if item.get('shopname'):
            shopname = item['shopname']
        if item.get('productionName'):
            production_name = item['productionName']

        item_detail = {
            'item_brand':brand,
            'item_name':item['name'],
            'item_category':category,
            'item_shop_name':shopname,
            'item_product_name':production_name,
            'item_url':item['url'],
            'item_product_id':item['productId'],
            'item_price':item['price'],
            'item_comment_count':item['commentCount'],
            'item_average_score':item['averageScore'],
            'item_show_evaluation_count':item['showCount'],
            'item_good_evaluation_count':item['goodCount'],
            'item_good_evaluation_rate':item['goodRate'],
            'item_general_evaluation_count':item['generalCount'],
            'item_general_evaluation_rate':item['generalRate'],
            'item_poor_evaluation_count':item['poorCount'],
            'item_poor_evaluation_rate':item['poorRate'],
            'item_date':item['date'],
            'update_time':datetime.datetime.utcnow(),
        }

        result = self.db['item_detail'].insert(item_detail)
        #item['mongodb_id'] = str(result)

        #log.msg("Item %s wrote to MongoDB database %s/item_detail" %
                    #(result, self.MONGODB_DB),
                    #level=log.DEBUG, spider=spider)
        return item

   
