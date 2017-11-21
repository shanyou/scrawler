# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MetaItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    status = scrapy.Field()     # 连载中 完本
    word = scrapy.Field()       # 字数
    update = scrapy.Field()     # 更新时间
    tclick = scrapy.Field()     # 总点击
    trecom = scrapy.Field()     # 总推荐
    chapter = scrapy.Field()    # dict ["chaptername": urls]


class ChapterItem(scrapy.Item):
    title = scrapy.Field()  # title
    name = scrapy.Field()    # chapter name
    num = scrapy.Field()    # chapter order
    content = scrapy.Field()    # content
