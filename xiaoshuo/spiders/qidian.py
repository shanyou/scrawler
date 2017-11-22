# -*- coding: utf-8 -*-
import scrapy
import re
import json
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
            yield Request(url=link.url, priority=PRIORITY_LOW, callback=self.process_info_0)

    def process_info_0(self, response):
        sel = Selector(response)
        item = MetaItem()
        item['title'] = sel.xpath('//div[contains(@class, "book-info")]/h1/em/text()').extract_first()
        item['author'] = sel.xpath('//div[contains(@class, "book-info")]/h1/span/a/text()').extract_first()
        item['desc'] = ''.join(sel.xpath('//div[contains(@class, "book-intro")]/node()/text()').extract()).strip()
        tags = sel.xpath('//p[contains(@class, "tag")]/a/text()').extract()
        author_tags = sel.css('a.tags').xpath('text()').extract()
        item['tags'] = tags + author_tags
        item['url'] = response.url
        item['status'] = sel.css('p.tag span').xpath('text()').extract_first()
        book_info = ''.join(sel.css("div.book-info p")[2].xpath(".//text()").extract()).strip()
        item['word'] = re.compile(u'[\S]+?\u4e07\u5b57').search(book_info).group()
        item['tclick'] = re.compile(u'[^|]+?\u4e07\u603b\u70b9\u51fb').search(book_info).group()
        item['trecom'] = re.compile(u'[^|]+?\u4e07\u603b\u63a8\u8350').search(book_info).group()

        # bookid
        bookId = re.compile("/info/([\d]+)").search(response.url).group(1)
        chapterList = response.headers.getlist('Set-Cookie')
        if not chapterList:
            # chapter info
            array = []
            el_chapter = sel.css("div.volume ul li")
            el_chapter.extract()
            for index, s in enumerate(el_chapter):
                ch = dict()
                ch['num'] = index + 1
                content_url = "http:" + s.xpath(".//a/@href").extract_first()
                ch['url'] = [content_url]
                ch['name'] = s.xpath('.//a/text()').extract_first()
                array.append(ch)

            if not array:
                print "chapter empty"
            item['chapter'] = array
            yield item
        else:
            csrfToken = response.headers.getlist('Set-Cookie')[0].split(';')[0]
            ajaxUrl = "https://book.qidian.com/ajax/book/category?" + csrfToken + "&bookId=" + bookId
            yield Request(ajaxUrl, meta={'item': item}, callback=self.process_info_1, priority=PRIORITY_MID)


    def process_info_1(self, response):
        if 'item' in response.meta:
            item = response.meta['item']
            array = dict()
            array['qidian'] = json.loads(response.body)
            item['chapter'] = array
            yield item
