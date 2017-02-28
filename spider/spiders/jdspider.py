#__author__ = 'duanla'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from spider.items import SpiderItem
#from spider.utils.select_result import list_first_item,strip_null,deduplication,clean_url
from scrapy.spiders import logging
from scrapy.http import Request
from urlparse import urljoin
import hashlib
import json
import requests
import time

search_base_url = "http://search.jd.com/search"
item_base_url = "http://item.jd.com/"
search_string = "search"
item_string = "item"
comment_string = "comments"
serachr_page_urls = {}
item_urls = {}

class JDSpider(CrawlSpider):
    name = 'jd'
    allowed_domains = ["jd.com"]
    
    
    start_urls = ["http://search.jd.com/Search?keyword=%E7%88%B1%E4%BB%96%E7%BE%8E1%E6%AE%B5&enc=utf-8&suggest=1.his.0&wq=&pvid=x9b072gi.xeo5ep"]
    #Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/top250\?start=\d+.*'))),
    #rules = [Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/top250\?start=\d+.*'))),
             #Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/subject/\d+')), callback="parse_item"),]


    def parse(self,response):
        sel = HtmlXPathSelector(response)
        links = sel.xpath(u'//a[@onclick]/@href').extract()

        for link in links:
            if link:
                link=urljoin(search_base_url,link)
                if search_string in link:
                    urlhash = hashlib.md5(link).hexdigest()
                    if not serachr_page_urls.has_key(urlhash):
                        serachr_page_urls[urlhash] = link
                        #logging.info(urlhash, level=log.DEBUG)
                        #logging.info(link.decode(response.encoding), level=log.DEBUG)
                
                if item_string in link:
                    if not comment_string in link:
                        urlhash = hashlib.md5(link).hexdigest()
                        if not item_urls.has_key(urlhash):
                            item_urls[urlhash] = link
                            #logging.info(urlhash, level=log.DEBUG)
                            #logging.info(link.decode(response.encoding), level=log.DEBUG)

        for search in serachr_page_urls.values():
            yield Request(url=search, callback=self.parse)

        for item in item_urls.values():
            yield Request(url=item, callback=self.parse_item)

        """if next_link:
            #next_link = clean_url(response.url,next_link,response.encoding)
            log.msg("Page's url : %s", next_link, level=log.DEBUG)
            yield Request(url=next_link, callback=self.parse)

        for detail_link in sel.select(u'//div[@class="p-name"]/a/@href').extract():
            if detail_link:
                yield Request(url=detail_link, callback=self.parse_item)"""


    def parse_item(self, response):
        sel = HtmlXPathSelector(response)
        item = SpiderItem()
        brandList = sel.xpath('//*[@id="root-nav"]/div/div/span[2]/a[1]/text()').extract()
        if len(brandList):
            item['brand'] = brandList[0]
        nameStr = sel.xpath('//*[@id="name"]/h1').xpath('string(.)').extract()[0]
        if nameStr:
            name_list = nameStr.split('\n')
        name = ''
        for i in name_list:
            name = name + i.strip('\t\n\r')
        # item['name'] = sel.xpath('//*[@id="name"]/h1/text()').extract()[0]
        item['name'] = name
        #type =
        #item['type'] = sel.xpath('').extract()
        category = sel.xpath('//*[@id="root-nav"]/div/div/span[1]/a[1]/text()').extract()
        if len(category):
            item['category'] = category[0]
        shopname = sel.xpath('//*[@id="extInfo"]/div[2]/a/text()').extract()
        if len(shopname):
            item['shopname'] = shopname[0]
        # item['productionName'] = sel.xpath('//*[@id="name"]/h1/text()').extract()[0]
        item['productionName'] = name
        item['url'] = response.url
        #price = sel.xpath('//*[@id="jd-price"]/text()').extract()
        #if len(price):
        #    item['price'] = price[0]
        split_for_id = item['url'].split('/')
        productId = split_for_id[len(split_for_id)-1].split('.')[0]
        print productId
        item['productId'] = productId
        '''Obtain image url'''
        imageUrlStr = sel.xpath('//*[@id="spec-n1"]/img/@src').extract()[0]
        if len(imageUrlStr):
            # item['imageUrl'] = imageUrlStr.split('//')[1]
            item['imageUrl'] = "http:" + imageUrlStr
        '''Obtain price'''
        priceUrl = "http://p.3.cn/prices/mgets?type=1&skuIds=J_" + productId
        #print priceUrl
        #sel1 = Request(priceUrl, callback=self.parsePrice)
        sel1 = requests.get(priceUrl)
        content = sel1.content #sel.text can also be used
        re = content.split('\n')
        price = json.loads(re[0])
        #log.msg("price is: " + price[0]["p"], level=log.INFO)
        if price[0]["p"]:
            item['price'] = price[0]["p"]
        '''Obtain comment'''
        commentUrl = "http://club.jd.com/clubservice/summary-m-" + productId + ".html"
        commentResponse = requests.get(commentUrl)
        commentStr = commentResponse.content.split('\n')
        commentJson = json.loads(commentStr[0])
        #log.msg("comment response: " + commentStr[0], level=log.INFO)
        if commentJson:
            commentSummary = commentJson["CommentsCount"][0]
            item['commentCount'] = commentSummary["CommentCount"]
            item['commentListPageNum'] = commentSummary["CommentCount"]/10 + 1
            item['averageScore'] = commentSummary["AverageScore"]
            item['goodCount'] = commentSummary["GoodCount"]
            item['goodRate'] = commentSummary["GoodRate"]
            item['generalCount'] = commentSummary["GeneralCount"]
            item['generalRate'] = commentSummary["GeneralRate"]
            item['poorCount'] = commentSummary["PoorCount"]
            item['poorRate'] = commentSummary["PoorRate"]
            item['showCount'] = commentSummary["ShowCount"]

        # log.msg(sel1.content,level=log.DEBUG)
        # log.msg(re, level=log.DEBUG)
        # log.msg(re[0], level=log.DEBUG)
        # print re
        # print re[0]
        #promotionInfo = sel.xpath('//*[@id="prom"]/div/em[2]').extract()[0]
        #item['promotionInfo'] = promotionInfo
        #item['monthlySalesVolume'] = sel.xpath().extract()[0]
        #item['evaluationNum'] = sel.xpath('//*[@id="comment-count"]/a/text()').extract()[0]
        #item['goodEvaluationNum'] = sel.xpath('//*[@id="comments-list"]/div[1]/div[1]/ul/li[2]/a/em/text()').extract()[0]
        item['date'] = time.strftime("%Y%m%d")
        return item

#sel.xpath('//html/body/div[5]/div[3]/div[8]/div//a/@href').extract()
###next page###
#sel.xpath(u'//a[@class="next"]/@href').extract()
# sel.xpath('//div[@class="p-price"]/strong/@data-price')[0].extract()
#sel.xpath('//a[@onclick]/@href')
