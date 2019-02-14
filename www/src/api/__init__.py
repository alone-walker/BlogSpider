# -*- coding: utf-8 -*-


from flask import Blueprint
from flask_restful import Api

from .feed import CrawlSpiders, AtomFeed, BlogFeed
from .db import Vote, Day, Categories, Entries, Spiders


__all__ = ['init_api']


def init_api(app):
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    api.add_resource(Day, '/api/day')
    api.add_resource(Entries, '/api/entries')
    api.add_resource(Categories, '/api/categories')
    api.add_resource(Spiders, '/api/spiders')
    api.add_resource(Vote, '/api/vote')
    api.add_resource(CrawlSpiders, '/submit/crawl')
    api.add_resource(AtomFeed, '/submit/rss')
    api.add_resource(BlogFeed, '/submit/blog')
    app.register_blueprint(api_bp)
