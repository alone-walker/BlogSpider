# -*- coding: utf-8 -*-


from ..model import is_exists_article, save_article
from ..ai import get_category


def get_article_lang(item):
    if any(ord(c) > 19967 for c in item['title']):
        return 'zh'
    return 'en'


class StorePipeline(object):

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def process_item(self, item, spider):
        if item is not None:
            item2 = dict(item)
            item2['lang'] = get_article_lang(item)
            item2['spider'] = spider._id
            item2['source'] = spider.title
            item2['category'] = get_category(item2)
            if not is_exists_article(item2):
                save_article(item2)
        return item
