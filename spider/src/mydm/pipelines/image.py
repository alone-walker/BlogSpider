# -*- coding: utf-8 -*-


import base64
import logging
import tempfile
from io import BytesIO
from urllib.parse import urlparse, urljoin

from lxml.html import HtmlElement
from PIL import Image as ImageLib, ImageFile

from scrapy.http import Request
from scrapy.pipelines.media import MediaPipeline

from mydm.util import is_url


logger = logging.getLogger(__name__)


ImageFile.LOAD_TRUNCATED_IMAGES = True


class Image:

    MAX_WIDTH = 1024

    def __init__(self, data, type=None):
        try:
            self._image = ImageLib.open(BytesIO(data))
        except OSError:
            if type not in ('PNG', 'JPG', 'JPEG'):
                raise
            fp = tempfile.NamedTemporaryFile(suffix=f'.{type}')
            fp.write(data)
            fp.seek(0)
            self._image = ImageLib.open(fp)

    @property
    def size(self):
        return self._image.size

    @property
    def type(self):
        return self._image.format

    def optimize(self, quality=75):
        image = self._image
        width, height = image.size
        if width > self.MAX_WIDTH:
            ratio = float(height) / float(width)
            width = self.MAX_WIDTH
            height = int(width * ratio)
            image = image.resize(
                    (width, height),
                    ImageLib.ANTIALIAS
            )
        buffer = BytesIO()
        image.save(
                buffer,
                format=self.type,
                quality=quality,
        )
        return buffer.getvalue()


class ImagesDlownloadPipeline(MediaPipeline):

    MEDIA_NAME = 'image'
    MAX_SIZE = 1024*256

    def __init__(self, settings):
        super().__init__(settings=settings)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        pipe = cls(settings)
        pipe.crawler = crawler
        return pipe

    @property
    def spider(self):
        return self.spiderinfo.spider

    @property
    def spider_name(self):
        return self.spiderinfo.spider.name

    def need_optimize(self, size):
        if size < self.MAX_SIZE:
            return False
        return True

    def get_media_requests(self, item, info):
        self._invalid_img_element = []
        doc = item['content']
        assert isinstance(doc, HtmlElement)
        attrs = {'src'}
        img_attr = getattr(
                self.spider,
                'image_url_attr',
                None,
        )
        if isinstance(img_attr, (list, tuple)):
            attrs = attrs.union(img_attr)
        elif img_attr:
            attrs.add(img_attr)

        urls = []
        for e in doc.xpath('//img'):
            for attr in attrs:
                if attr not in e.attrib:
                    continue
                url = e.get(attr).strip('\t\n\r ')
                if url.startswith('//'):
                    r = urlparse(item['link'])
                    url = r.scheme + url
                elif url.startswith('/'):
                    url = urljoin(item['link'], url)
                if not is_url(url):
                    continue
                else:
                    urls.append((url, e))
                    break
            else:
                logger.error(
                        "spider[%s] can't find image link attribute",
                        self.spider_name
                )

        requests = []
        for url, e in urls:
            if url.startswith('data'):
                continue
            try:
                r = Request(url, meta={'image_xpath_node': e})
            except ValueError:
                logger.error(
                        'spider[%s] got invalid url[%s]',
                        self.spider_name,
                        url
                )
            else:
                requests.append(r)
        return requests

    def media_failed(self, failure, request, info):
        logger.error(
                'spider[%s] download image[%s] failed',
                self.spider_name,
                request.url
        )

    def media_downloaded(self, response, request, info):
        if not response.body:
            logger.error(
                    'spider[%s] got size 0 image[%s]',
                    self.spider_name,
                    request.url
            )
            self._invalid_img_element.append(
                    response.meta['image_xpath_node']
            )
            return
        image_xpath_node = response.meta['image_xpath_node']
        src = response.url
        data = response.body
        image_size = len(data)
        try:
            image_type = response.headers[
                    'Content-Type'
                    ].split('/')[-1].upper()
        except KeyError:
            image_type = src.split('.')[-1].upper()
        try:
            image = Image(data, type=image_type)
        except (OSError, IOError) as e:
            logger.error(
                    'spider[%s] PILLOW open image[%s] failed[%s]',
                    self.spider_name,
                    src,
                    e
            )
        else:
            if self.need_optimize(image_size):
                data = image.optimize()
            image_type = image.type.upper()
        image_xpath_node.set('source', src)
        data = base64.b64encode(data).decode('ascii')
        image_xpath_node.set(
                'src',
                f'data:image/{image_type};base64,{data}'
        )

    def item_completed(self, results, item, info):
        for e in self._invalid_img_element:
            e.drop_tree()
        self._invalid_img_element = []
        return item
