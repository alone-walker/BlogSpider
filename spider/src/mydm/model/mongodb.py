# -*- coding: utf-8 -*-


from datetime import datetime

from pymongo import MongoClient, ASCENDING
from scrapy.utils.project import get_project_settings


class MongoDB:

    def __init__(self):
        self._db = None

    def _create_indexes(self):
        db = self._db
        feed = db['feed']
        feed.create_index('url', name='idx_url')
        article = db['article']
        article.create_index('crawl_date', name='idx_crawl_date')
        article.create_index(
                [('spider', ASCENDING), ('crawl_date', ASCENDING)],
                name='idx_spider_crawl_date'
        )
        scrapecount = db['scrapecount']
        scrapecount.create_index('spider', name='idx_spider')

    def _connect(self):
        settings = get_project_settings()
        client = MongoClient(settings['MONGODB_URI'], connect=False)
        db = client[settings['MONGODB_DB_NAME']]
        db.authenticate(settings['MONGODB_USER'], settings['MONGODB_PWD'])
        self._db = db
        self._create_indexes()

    def __getattr__(self, key):
        if self._db is None:
            self._connect()
        try:
            return self._db[key]
        except KeyError:
            raise AttributeError(f'collection[{key}] not found')


ScrapyDB = MongoDB()


def is_exists_feed(url):
    cursor = ScrapyDB.feed.find({'url': url}).limit(1)
    if cursor.count() == 0:
        return False
    else:
        return True


def save_feed(url):
    result = ScrapyDB.feed.insert_one(
        {
            'url': url,
            'create_date': datetime.now()
        }
    )
    return result.inserted_id


def _get_day_begin(item):
    d = item['crawl_date']
    t = datetime(
            d.year,
            d.month,
            d.day,
            0,
            0,
            0,
            0
    )
    return t


def is_exists_article(item):
    t = _get_day_begin(item)
    cursor = ScrapyDB.article.find(
        {
            'spider': item['spider'],
            'crawl_date': {'$lt': t},
            'title': item['title'],
            'domain': item['domain'],
            'source': item['source']
        }
    ).limit(1)
    if cursor.count() > 0:
        return True
    cursor = ScrapyDB.article.find(
        {
            'spider': item['spider'],
            'crawl_date': {'$gte': t},
            'title': item['title']
        },
        {
            'content': 1
        }
    ).limit(1)
    if (cursor.count() > 0 and
       len(cursor[0]['content']) > len(item['content'])):
        return True
    return False


def save_article(item):
    t = _get_day_begin(item)
    result = ScrapyDB.article.update(
        {
            'spider': item['spider'],
            'crawl_date': {'$gte': t},
            'title': item['title']
        },
        item,
        upsert=True
    )
    return result


def is_exists_spider(url):
    cursor = ScrapyDB.spider.find(
            {
                'start_urls': {'$in': [url]}
            }
    )
    if cursor.count() == 0:
        return False
    else:
        return True


def save_spider_settings(settings):
    try:
        del settings['_id']
    except KeyError:
        pass
    result = ScrapyDB.spider.insert_one(settings)
    return result.inserted_id


def get_spider_settings():
    settings = []
    cursor = ScrapyDB.spider.find()
    for item in cursor:
        setting = dict(item)
        setting['_id'] = str(item['_id'])
        settings.append(setting)
    return settings


def get_category_tags():
    cursor = ScrapyDB.category.find()
    return {
            item['category']: item['tags']
            for item in cursor
    }


def log_spider_scrape_count(spider, count):
    result = ScrapyDB.scrapecount.insert_one(
        {
            'spider': spider._id,
            'time': datetime.now(),
            'count': count,
        }
    )
    return result.inserted_id
