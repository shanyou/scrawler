# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from xiaoshuo.items import *


class XiaoshuoPipeline(object):
    root_dir = "novel"
    
    def process_item(self, item, spider):
        if isinstance(item, MetaItem):
            return self.process_meta(item, spider)
        elif isinstance(item, ChapterItem):
            return self.process_chapter(item, spider)
        return item

    def process_meta(self, meta, spider):
        """
        process meta data
        :param meta:
        :param spider:
        :return:
        """
        pass

    def process_chapter(self, chapter, spider):
        """
        process chapter data
        :param chapter:
        :param spider:
        :return:
        """
        pass