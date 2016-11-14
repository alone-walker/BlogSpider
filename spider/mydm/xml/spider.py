# -*- coding: utf-8 -*-


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from datetime import datetime
from lxml import etree

from scrapy import Request

from ..log import logger
from .extractor import ItemExtractor
from ..items import ArticleItem
from ..spider import ErrbackSpider


class LXMLSpider(ErrbackSpider):
    """
    Tags item must contain
    """
    TAGS = ('title', 'link', 'content')

    def check_item(self, item):
        return True if all(k in item and item[k] is not None
                           for k in self.TAGS) else False

    def has_content_extractor(self):
        return True if hasattr(self, 'item_content_xpath') else False

    def extract_content(self, response):
        item = response.meta['item']
        content = response.xpath(self.item_content_xpath).extract_first()
        if content is not None:
            item['content'] = content
            item['encoding'] = response.encoding
            item['link'] = response.url
        else:
            logger.error('spider[{}] extract content failed'.format(self.name))
        return ArticleItem(item)

    def parse(self, response):
        parser = etree.XMLParser(ns_clean=True,
                                 recover=True,
                                 encoding=response.encoding)
        root = etree.XML(response.body, parser)
        while len(root) == 1:
            root = root[0]
        for entry in root:
            item = ItemExtractor()(entry)
            item['category'] = self.category
            item['crawl_date'] = datetime.now()
            item['domain'] = urlparse(response.request.url).netloc
            item['data_type'] = 'html'
            item['encoding'] = response.encoding
            if self.check_item(item):
                if self.has_content_extractor():
                    yield Request(item['link'],
                                  callback=self.extract_content,
                                  meta={'item': item})
                else:
                    yield ArticleItem(item)


class LXMLSpiderMeta(type):
    def __new__(cls, name, bases, attrs):
        ATTRS = ['start_urls',
                 'category',
                 'name']
        if all(attr in attrs for attr in ATTRS):
            return super(LXMLSpiderMeta, cls).__new__(cls, name, bases, attrs)
        else:
            raise AttributeError


def mk_lxmlspider_cls(sp_setting):
    return LXMLSpiderMeta('{}Spider'.format(sp_setting['name']),
                          (LXMLSpider,),
                          sp_setting)
