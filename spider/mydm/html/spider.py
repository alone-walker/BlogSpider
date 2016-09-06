# -*- coding: utf-8 -*-


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from datetime import datetime
import inspect
import logging

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request

from ..items import ArticleItem
from ..ai import TagExtractor


logger = logging.getLogger(__name__)


class BLOGSpiderException(Exception):
    pass


class BLOGSpider(Spider):
    """
    tags item must contain
    """
    TAGS = ('title', 'link', 'content')

    def check_item(self, item):
        return True if all(tag in item and item[tag] is not None
                           for tag in self.TAGS) else False

    def extract_entries(self, response):
        return Selector(response, type='html').xpath(self.entry_xpath)

    def extract_item(self, entry):
        attrs = inspect.getmembers(self.__class__,
                                   lambda a: not(inspect.isroutine(a)))
        extractors = [attr for attr in attrs
                      if attr[0].startswith('item_') and
                      attr[0].endswith('_xpath') and
                      attr[0] != 'item_content_xpath']
        item = {name.split('_')[1]: entry.xpath(xnode).extract_first()
                for name, xnode in extractors}
        tags = TagExtractor()(entry.xpath('.').extract_first())
        if tags is not None:
            item['tag'] = tags
        return item

    def extract_content(self, response):
        item = response.meta['item']
        tags = TagExtractor()(response.text)
        if tags is not None:
            item['tag'] = tags
        item['encoding'] = response.encoding
        item['link'] = response.url
        content = response.xpath(self.item_content_xpath).extract_first()
        item['content'] = content
        if self.check_item(item):
            return ArticleItem(item)
        else:
            miss_tags = [tag for tag in self.TAGS
                         if tag not in item or item[tag] is None]
            logger.error(
                '{} extract content error, miss tags: {}'.format(self.name,
                                                                 miss_tags))
            raise BLOGSpiderException(
                '{} extract content error'.format(self.name))

    def parse(self, response):
        try:
            prelink = response.xpath(self.link_pre_xpath).extract_first()
            yield Request(prelink, callback=self.parse)
        except AttributeError:
            logger.info('{} has no prelink attr'.format(self.name))

        for entry in self.extract_entries(response):
            item = self.extract_item(entry)
            item['category'] = self.category
            item['crawl_date'] = datetime.now()
            item['domain'] = urlparse(response.request.url).netloc
            item['data_type'] = 'html'
            link = item['link'].strip()
            if link is None:
                continue
            if not link.startswith('http'):
                item['link'] = response.urljoin(link)
            yield Request(item['link'],
                          callback=self.extract_content,
                          meta={'item': item})


class BLOGSpiderMeta(type):
    def __new__(cls, name, bases, attrs):
        ATTRS = ['start_urls',
                 'category',
                 'item_title_xpath',
                 'item_link_xpath',
                 'item_content_xpath']
        if all(attr in attrs for attr in ATTRS):
            return super(BLOGSpiderMeta, cls).__new__(cls, name, bases, attrs)
        else:
            raise AttributeError


def mk_blogspider_cls(sp_setting):
    return BLOGSpiderMeta('{}Spider'.format(sp_setting['name']),
                          (BLOGSpider,),
                          sp_setting)
