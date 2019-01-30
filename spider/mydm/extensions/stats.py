# -*- coding: utf-8 -*-


import logging

from scrapy import signals

from ..model import log_spider_scraped_count


logger = logging.getLogger(__name__)


class ExtensionStats:

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.stats)
        crawler.signals.connect(
                ext.spider_closed,
                signal=signals.spider_closed
        )
        return ext

    def spider_closed(self, spider):
        item_scraped_count = self.stats.get_value('item_scraped_count', 0)
        logger.info(
                f'spider[{spider.name}] crawled {item_scraped_count} articles'
        )
        log_spider_scraped_count(spider, item_scraped_count)
