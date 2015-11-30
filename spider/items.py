# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class SpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand = Field()
    name = Field()
    type = Field()
    category = Field()
    shopname = Field()
    productionName = Field()
    productId = Field()
    url = Field()
    price = Field()
    promotionInfo = Field()
    monthlySalesVolume = Field()
    evaluationNum = Field()
    #goodEvaluationNum = Field()
    date = Field()
    commentCount = Field()
    averageScore = Field()
    goodCount = Field()
    goodRate = Field()
    generalCount = Field()
    generalRate = Field()
    poorCount = Field()
    poorRate = Field()
    showCount = Field()#the comment with picture
    commentListPageNum = Field()
    imageUrl = Field()
    imagePath = Field()
