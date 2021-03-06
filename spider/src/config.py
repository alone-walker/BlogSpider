# -*- coding: utf-8 -*-

# scrapy settings
BOT_NAME = 'BlogSpider'
SPIDER_LOADER_CLASS = 'mydm.spiderloader.MongoSpiderLoader'

CONCURRENT_ITEMS = 64
CONCURRENT_REQUESTS = 12
CONCURRENT_REQUESTS_PER_DOMAIN = 4
DNS_TIMEOUT = 180
DOWNLOAD_DELAY = 1

WEBSERVICE_ENABLED = False
TELNETCONSOLE_ENABLED = False

LOG_ENABLED = True
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s-%(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

EXTENSIONS = {
        'mydm.extensions.ExtensionStats': 900
}

ITEM_PIPELINES = {
    'mydm.pipelines.ContentPipeline': 255,
    'mydm.pipelines.ImagesDlownloadPipeline': 300,
    'mydm.pipelines.StorePipeline': 999
}

DOWNLOADER_MIDDLEWARES = {
    # 'mydm.middlewares.ETagMiddleware': 300
}

"""
spider settings
"""

LOGGER_NAME = 'mydm'

# grpc
GRPC_URI = '[::]:50051'

# mongodb
MONGODB_URI = 'mongodb://mongodb:27017/'
MONGODB_DB_NAME = 'scrapy'
# MONGODB_ARTICLE_COLLECTION_NAME = 'article'
# MONGODB_FEED_COLLECTION_NAME = 'feed'
# MONGODB_SPIDER_COLLECTION_NAME = 'spider'
# MONGODB_SCRAPECOUNT_CONNECTION_NAME = 'scrapecount'
MONGODB_USER = 'scrapy'
MONGODB_PWD = 'scrapy'

# redis
ETAG_URL = 'redis://redis:6379/1'
TEMP_SPIDER_STATS_URL = 'redis://redis:6379/2'

# if-modify-since middleware
MODIFY_DELTA = 1

# image pipeline
IMAGE_OPTIMIZE_CATEGORY_FILTER = ['漫画']
