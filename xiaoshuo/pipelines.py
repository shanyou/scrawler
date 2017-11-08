# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from xiaoshuo.items import *
from functools import wraps
import os


def run_once(f):
    """Runs a function (successfully) only once.
    The running can be reset by setting the `has_run` attribute to False
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            result = f(*args, **kwargs)
            wrapper.has_run = True
            return result
    wrapper.has_run = False
    return wrapper


class XiaoshuoPipeline(object):
    root_dir = "novel"

    @run_once
    def __init_root(self):
        """
        init root directory for the pipeline
        :return:
        """
        d = os.path.join(os.getcwd(), self.root_dir)
        if not os.path.exists(d):
            os.makedirs(d)

    def __init__(self):
        self.__init_root()

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
