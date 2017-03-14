# -*- coding: utf-8 -*-


import logging
import re

from lxml.html import fromstring, HTMLParser, HtmlElement


logger = logging.getLogger(__name__)


class ReExtractor:
    p = re.compile(r'(tags\s*:|Fileds?\s*under\s*:|Tagged\s*with)\s*(.*)',
                   re.IGNORECASE)

    def __call__(self, doc):
        matches = self.p.findall(doc.text_content())

        def extract(s):
            s = re.sub(r'(\s|\t|\r|\n)+',
                       ' ',
                       s)
            tags = []
            for _ in s.split(','):
                tag = _.strip()
                if tag:
                    tags.append(tag)
            return tags

        if len(matches) == 1:
            s = matches[0][1]
            tags = extract(s)
            if tags:
                return tags
        elif len(matches) == 2:
            for _, s in matches:
                tags = extract(s)
                if tags:
                    return tags
        elif len(matches) > 2:
            s = matches[0][1]
            tags = extract(s)
            if tags:
                return tags
            s = matches[-1][1]
            tags = extract(s)
            if tags:
                return tags


class LXMLExtractor:
    p = re.compile(r'^\s*(tags\s*:|Fileds?\s*under\s*:|Tagged\s*with)\s*$',
                   re.IGNORECASE)

    def __call__(self, doc):
        for e in doc.xpath('//*[count(child::*)=0]'):
            if self.p.match(e.text_content()) is not None:
                container = e.getparent()
                for idx, _ in enumerate(container):
                    if _ is e:
                        break
                tags = []
                for _ in container[idx+1:]:
                    tag = _.text_content().strip('\r\n\t\s')
                    if tag:
                        tags.append(tag)
                return tags


class TagExtractor:
    EXTRACTORS = (ReExtractor, LXMLExtractor)

    def __call__(self, doc, encoding='UTF-8'):
        if isinstance(doc,
                      (str, bytes)):
            doc = fromstring(bytes(bytearray(doc,
                                             encoding=encoding)),
                             parser=HTMLParser(encoding=encoding))
        if not isinstance(doc,
                          HtmlElement):
            return None
        for cls in self.EXTRACTORS:
            extract = cls()
            tags_ = extract(doc)
            if tags_:
                tags = []
                for idx, tag in enumerate(tags_):
                    if idx < 2 and len(tag) > 16:
                        break
                    elif len(tag) < 16:
                        tags.append(tag)
                else:
                    if tags:
                        logger.info('TagExtractor got tags %s',
                                    tags)
                    return tags


def extract_tags(doc, encoding):
    extract = TagExtractor()
    return extract(doc,
                   encoding=encoding)
