# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from xiaoshuo.items import *
from urllib2 import urlparse


class QuanbenSpider(CrawlSpider):
    name = 'quanben'
    allowed_domains = ['quanben.io']
    base_domain = 'http://quanben.io'
    start_urls = ['http://quanben.io/']

    rules = (
        Rule(sle(allow=r'/c/'), callback=None, follow=True),
        Rule(sle(allow=r'/n/'), callback="parse_book_0", follow=False),
        Rule(sle(allow=r'/c/[^_]+_[\d]+.html$'), callback=None, follow=True) # next page
    )

    def parse_book_0(self, response):
        """
        find content list from http://quanben.io/n/xianni/
        :param response:
        :return: new request
        """
        url = urlparse.urljoin(self.base_domain, response.xpath('//a[contains(@itemprop,"url")]/@href').extract()[0])
        return Request(url, callback=self.parse_book_1)

    def parse_book_1(self, response):
        sel = Selector(response)
        item = XiaoshuoItem()
        item['title'] = sel.xpath('//h1/text()').extract()
        item['category'] = sel.xpath('//span[contains(@itemprop,"category")]/text()').extract()
        item['author'] = sel.xpath('//span[contains(@itemprop,"author")]/text()').extract()
        yield item
