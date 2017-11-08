# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from xiaoshuo.items import *
from xiaoshuo.misc import *
from urllib2 import urlparse
import re
import urllib


class QuanbenSpider(CrawlSpider):
    name = 'quanben'
    allowed_domains = ['quanben.io']
    base_domain = 'http://quanben.io'
    post_url = 'http://quanben.io/index.php?c=book&a=ajax'
    start_urls = ['http://quanben.io/']
    # start_urls = ['http://quanben.io/n/wankuzongshoureshanggong/140.html']

    rules = (
        Rule(sle(allow=r'/c/'), callback=None, follow=True),
        Rule(sle(allow=r'/n/'), callback="parse_book_0", follow=False),
        Rule(sle(allow=r'/c/[^_]+_[\d]+.html$'), callback=None, follow=True),   # next page
        # Rule(sle(allow=r'/n/[^/]+/[\d]+.html$'), callback="parse_content_0", follow=False),  # next page
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
        item = MetaItem()
        item['title'] = sel.xpath('//h1/text()').extract_first()
        item['category'] = sel.xpath('//span[contains(@itemprop,"category")]/text()').extract_first()
        item['author'] = sel.xpath('//span[contains(@itemprop,"author")]/text()').extract_first()
        item['desc'] = sel.xpath('//div[contains(@itemprop, "description")]/node()').extract_first()
        # find chapter
        el_chapter = sel.xpath('//li[contains(@itemprop, "itemListElement")]/node()')
        el_chapter.extract()
        array = []

        for index, s in enumerate(el_chapter):
            ch = dict()
            ch['num'] = index + 1
            content_url = urlparse.urljoin(self.base_domain, s.xpath('@href').extract()[0])
            ch['url'] = content_url
            ch['name'] = s.xpath('span/text()').extract_first()
            array.append(ch)
            yield Request(content_url, meta={'chapter': ch}, callback=self.parse_content_0)

        item['chapter'] = array
        yield item

    def parse_content_0(self, response):
        sel = Selector(response)
        item = ChapterItem()
        if 'chapter' in response.meta:
            ch = response.meta['chapter']
            item['num'] = ch['num']
        title = sel.css('div.name::text').extract_first()
        item['title'] = title
        item['name'] = sel.css('h1.headline::text').extract_first()

        # find content
        content_s = sel.xpath("//div[@itemprop='articleBody']/script")
        content_s.extract()
        len = content_s.__len__() or 1
        script = content_s[len-1].xpath("text()").extract_first().encode("utf-8")
        frmdata = dict()
        pinyin = re.compile(r'pinyin\',\'([^\']+)').search(script).group(1)
        id = re.compile(r'id\',\'([^\']+)').search(script).group(1)
        sky = re.compile(r'sky\',\'([^\']+)').search(script).group(1)
        t = re.compile(r't\',\'([^\']+)').search(script).group(1)
        rnd = now_milliseconds()
        frmdata["pinyin"] = pinyin
        frmdata["id"] = id
        frmdata["sky"] = sky
        frmdata["t"] = t
        frmdata["_type"] = "ajax"
        frmdata["rndval"] = rnd

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        yield Request(self.post_url, meta={"item": item}, callback=self.parse_content_1, method="POST", headers=headers, body=urllib.urlencode(frmdata))

    def parse_content_1(self, response):
        if 'item' in response.meta:
            sel = Selector(response)
            item = response.meta['item']
            item['content'] = sel.xpath("//body//text()").extract()
            return item



