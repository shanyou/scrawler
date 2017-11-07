# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MetaItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    chapter = scrapy.Field()    # dict ["chaptername": url]


class ChapterItem(scrapy.Item):
    title = scrapy.Field()  # title
    chapter = scrapy.Field()    # chapter name
    num = scrapy.Field()    # chapter order
    content = scrapy.Field()    # content
