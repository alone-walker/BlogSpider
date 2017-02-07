# -*- coding: utf-8 -*-


import logging
import re
import json
import uuid
import random
from urllib.parse import urlparse

from requests.exceptions import ConnectionError
import requests
import redis
import pika
from lxml import etree

from twisted.internet import reactor, defer

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from mydm.model import save_spider_settings, save_feed, is_exists_spider
from mydm.spiderfactory import SpiderFactory, SpiderFactoryException
from mydm.util import parse_redis_url

logger = logging.getLogger(__name__)

SETTINGS = get_project_settings()


def _send(key, data):
    body = json.dumps(data)
    connection = pika.BlockingConnection(
        pika.connection.URLParameters(SETTINGS['BROKER_URL']))
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs',
                             type='direct')
    channel.basic_publish(exchange='direct_logs',
                          routing_key=key,
                          body=body)
    connection.close()


def get_feed_name(url):
    parser = urlparse(url)
    fields = parser.hostname.split('.')
    if len(fields) == 1:
        return re.sub(r'[^a-zA-Z]',
                      '',
                      fields[0]
                      ).lower().capitalize()
    else:
        return ''.join([re.sub(r'[^a-zA-Z]',
                               '',
                               _).lower().capitalize()
                        for _ in fields[:-1] if _.lower() != 'www'])


def test_spider(setting):
    setting = setting.copy()
    spid = str(uuid.uuid4())
    setting['_id'] = spid
    try:
        cls = SpiderFactory.mkspider(setting)
    except SpiderFactoryException as e:
        logger.error('{}'.format(e))
        return False
    url = SETTINGS['TEMP_SPIDER_STATS_URL']
    TEST_SETTINGS = {'ITEM_PIPELINES': {'mydm.pipelines.StatsPipeline': 255},
                     'SPIDER_STATS_URL': url,
                     'BOT_NAME': 'TestSpider',
                     'WEBSERVICE_ENABLED': False,
                     'TELNETCONSOLE_ENABLED': False,
                     'LOG_LEVEL': 'INFO',
                     'LOG_FORMAT': '%(asctime)s-%(levelname)s: %(message)s',
                     'LOG_DATEFORMAT': '%Y-%m-%d %H:%M:%S'}

    configure_logging(TEST_SETTINGS,
                      install_root_handler=False)
    logging.getLogger('scrapy').setLevel(logging.WARNING)
    runner = CrawlerRunner(TEST_SETTINGS)
    d = runner.crawl(cls)
    d.addBoth(lambda _: reactor.stop())
    logger.info('test_spider reator starting ...')
    reactor.run()
    logger.info('test_spider reator stopped')

    def get_stats(url, spid):
        conf = parse_redis_url(url)
        r = redis.Redis(host=conf.host,
                        port=conf.port,
                        db=conf.database)
        n = r.get(spid)
        r.delete(spid)
        return 0 if n is None else int(n)

    n = get_stats(url,
                  spid)
    return True if n > 0 else False


def gen_lxmlspider(setting):
    url = setting['url']
    del setting['url']
    save_feed(url)
    try:
        r = requests.get(url,
                         headers=SETTINGS['DEFAULT_REQUEST_HEADERS'])
    except ConnectionError:
        logger.error('Error in gen_lxmlspider connection[%s]',
                     url)
        return False
    if r.status_code != 200:
        logger.error('Error in gen_lxmlspider requests[%s, status=%d]',
                     url,
                     r.status_code)
        return False

    parser = etree.XMLParser(ns_clean=True)
    root = etree.XML(r.content,
                     parser)
    while len(root) == 1:
        root = root[0]
    for e in root:
        try:
            en = etree.QName(e.tag).localname.lower()
        except ValueError:
            continue
        else:
            if en == 'title':
                setting['title'] = re.sub(r'^(\r|\n|\s)+|(\r|\n|\s)+$',
                                          '',
                                          e.text)
    setting['name'] = get_feed_name(url)
    if 'title' not in setting:
        setting['title'] = setting['name']
    setting['type'] = 'xml'
    setting['start_urls'] = [url]
    if is_exists_spider(url):
        return True
    if test_spider(setting):
        save_spider_settings(setting)
        return True
    else:
        logger.error('Error in gen_lxmlspider[%s]',
                     url)
        return False


def gen_blogspider(setting):
    url = setting['url']
    del setting['url']
    save_feed(url)
    setting['name'] = get_feed_name(url)
    setting['title'] = setting['name']
    setting['type'] = 'blog'
    setting['start_urls'] = [url]
    if is_exists_spider(url):
        return True
    if test_spider(setting):
        save_spider_settings(setting)
        return True
    else:
        logger.error('Error in gen_blogspider[%s]',
                     url)
        return False


def _get_failed_spiders(spids):
    conf = parse_redis_url(SETTINGS['SPIDER_STATS_URL'])
    r = redis.Redis(host=conf.host,
                    port=conf.port,
                    db=conf.database)

    def get_stats(spid):
        n = r.get(spid)
        return 0 if n is None else int(n)

    return [_ for _ in spids if 0 == get_stats(_)]


def _flush_db():
    conf = parse_redis_url(SETTINGS['SPIDER_STATS_URL'])
    r = redis.Redis(host=conf.host,
                    port=conf.port,
                    db=conf.database)
    r.flushdb()


def crawl(args):
    spids = args.get('spiders')
    configure_logging(SETTINGS,
                      install_root_handler=False)
    logging.getLogger('scrapy').setLevel(logging.WARNING)
    runner = CrawlerRunner(SETTINGS)
    loader = runner.spider_loader
    if 'all' in spids:
        spiders = [loader.load(_) for _ in loader.list()]
    else:
        spiders = [loader.load(_)
                   for _ in filter(lambda __: __ in loader.list(),
                                   spids)]
    if not spiders:
        return False

    for __ in random.shuffle(spiders):
        runner.crawl(__)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    _flush_db()
    logger.info('crawl reator starting ...')
    reactor.run()
    logging.info('crawl reator stopped')

    if len(spiders) > 4:
        failed_spiders = _get_failed_spiders(spids)
        if failed_spiders:
            _send(SETTINGS['CRAWL2_KEY'],
                  {'spiders': failed_spiders})


def crawl2(args):
    spids = args.get('spiders')
    configure_logging(SETTINGS,
                      install_root_handler=False)
    logging.getLogger('scrapy').setLevel(logging.WARNING)
    runner = CrawlerRunner(SETTINGS)
    loader = runner.spider_loader
    spiders = [loader.load(_) for _ in spids]
    if not spiders:
        return False

    @defer.inlineCallbacks
    def seqcrawl():
        for __ in random.shuffle(spiders):
            yield runner.crawl(__)
    seqcrawl()
    reactor.run()
