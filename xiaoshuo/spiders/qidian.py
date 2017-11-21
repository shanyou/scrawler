# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector
from xiaoshuo.items import *
PRIORITY_LOW = 10
PRIORITY_MID = 100
PRIORITY_HIGH = 1000


class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['qidian.com']
    start_urls = ['https://www.qidian.com/all']

    def parse(self, response):
        # extract next page
        sel = Selector(response)
        next_url = sel.xpath('//li/a[contains(@class, "lbf-pagination-next")]/@href').extract_first()
        if next_url is not None:
            yield Request(url="https:" + next_url, priority=PRIORITY_HIGH, callback=self.parse)

        # extract info page
        lx = LinkExtractor(allow=r'book.qidian.com/info/')
        links = lx.extract_links(response)
        for link in links:
            yield Request(url=link.url, priority=PRIORITY_LOW, callback=self.process_info)

    def process_info(self, response):
        sel = Selector(response)
        item = MetaItem()
        item['title'] = sel.xpath('//div[contains(@class, "book-info")]/h1/em/text()').extract_first()
        item['author'] = sel.xpath('//div[contains(@class, "book-info")]/h1/span/a/text()').extract_first()
        yield item
