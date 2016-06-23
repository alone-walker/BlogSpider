# -*- coding: utf-8 -*-


from dateutil.parser import parse as get_date
from lxml.etree import QName
from zope.interface import Interface, implementer


class ITagExtractor(Interface):
    def match(self, e):
        """ check if the element  match the tag """

    def extract(self, e):
        """ extract data from element """


@implementer(ITagExtractor)
class TitleTag(object):
    tag = 'title'

    def __init__(self):
        self.val = None

    def match(self, e):
        name = QName(e.tag).localname.lower()
        return name == 'title'

    def extract(self, e):
        if e.text is not None:
            self.val = e.text


@implementer(ITagExtractor)
class LinkTag(object):
    tag = 'link'

    def __init__(self):
        self.val = None

    def match(self, e):
        name = QName(e.tag).localname.lower()
        return name == 'link'

    def extract(self, e):
        if 'href' in e.attrib:
            v = e.attrib['href']
        else:
            v = e.text
        if v is not None:
            self.val = v.strip('\n ')


@implementer(ITagExtractor)
class PubDateTag(object):
    tag = 'pub_date'

    def __init__(self):
        self.val = None

    def match(self, e):
        name = QName(e.tag).localname.lower()
        return name in ('pubdate', 'updated')

    def extract(self, e):
        if e.text is None:
            return
        v = get_date(e.text)
        if self.val is None or self.val < v:
            self.val = v


@implementer(ITagExtractor)
class CategoryTag(object):
    tag = 'tag'

    def __init__(self):
        self.val = None

    def match(self, e):
        name = QName(e.tag).localname.lower()
        return name == 'category'

    def extract(self, e):
        if e.text is None:
            return
        if self.val is None:
            self.val = []
        self.val.append(e.text)


@implementer(ITagExtractor)
class ContentTag(object):
    tag = 'content'

    def __init__(self):
        self.val = None

    def match(self, e):
        name = QName(e.tag).localname.lower()
        return name in ('encoded', 'description', 'content', 'summary')

    def extract(self, e):
        if e.text is None:
            return
        if self.val is None or len(self.val) < len(e.text):
            self.val = e.text


class ItemExtractor(object):
    def __init__(self):
        self.extractors = [TitleTag(),
                           LinkTag(),
                           PubDateTag(),
                           CategoryTag(),
                           ContentTag()]

    def __call__(self, entry):
        for e in entry:
            for i in self.extractors:
                try:
                    if i.match(e):
                        i.extract(e)
                        break
                except ValueError:
                    continue
        return {i.tag: i.val for i in self.extractors if i.val is not None}
