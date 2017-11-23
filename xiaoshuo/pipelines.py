# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from xiaoshuo.items import *
from functools import wraps
import os
import codecs
import json


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


def normalize_path(path):
    return path


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
        if not isinstance(meta, MetaItem):
            return
        title = meta['title']
        d = normalize_path(os.path.join(os.getcwd(), self.root_dir, title))
        if not os.path.exists(d):
            os.makedirs(d)
        meta_f = os.path.join(d, "meta.json")
        if not os.path.exists(meta_f):
            f = codecs.open(meta_f, 'w', encoding='utf-8')
            line = json.dumps(dict(meta), ensure_ascii=False)
            f.write(line)
            f.close()

    def process_chapter(self, chapter, spider):
        """
        process chapter data
        :param chapter:
        :param spider:
        :return:
        """
        if not isinstance(chapter, ChapterItem):
            return

        title = chapter['title']
        d = normalize_path(os.path.join(os.getcwd(), self.root_dir, title))
        if not os.path.exists(d):
            os.makedirs(d)
        name = chapter['name']
        num = str(chapter['num'])
        content_f = normalize_path(os.path.join(d, num + "_" + name + ".txt"))
        if not os.path.exists(content_f):
            f = codecs.open(content_f, 'w', encoding='utf-8')
            f.write(chapter['name'])
            for line in chapter['content']:
                f.write(line + "\n")
            f.close()
