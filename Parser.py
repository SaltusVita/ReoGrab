'''
Created on 10 июл. 2016 г.

@author: garet
'''

import lxml.html


class HtmlItem:
    def __init__(self, item, base_url=''):
        item_type = type(item)
        if item_type is str or item_type is bytes:
            self._item = lxml.html.document_fromstring(item)
        elif item_type is lxml.html.HtmlElement:
            self._item = item
        elif item_type is HtmlItem:
            self = item  # TODO: Переделать!
        elif item_type is None:
            self._item = lxml.html.HtmlElement()

    def type_find(self, s: str):
        return 'css'  # TODO: Доделать проверку типа поиска

    def find_items(self, s: str):
        type_find = self.TypeFind(s)
        result = None
        if type_find == 'xpath':
            result = self._item.xpath(s)
        elif type_find == 'css':
            result = self._item.cssselect(s)
        return result

    def find(self, s: str, number=0):
        result = self.find_items(s)
        if result is None:
            return HtmlItem(result)
        if len(result) >= number:
            return HtmlItem(result[number])
        return HtmlItem(result.pop())

    def find_all(self, s: str, start=0, lenght=-1):
        result = self.find_items(s)
        return HtmlItems(result)

    def text(self, strip=True):
        result = ''.join(self._item.itertext())
        if strip:
            return result.strip()
        elif type(strip) == str:
            return result.strip(strip)
        return result

    def Href(self, strip=True):
        return self.attr('href', strip)

    def src(self, strip=True):
        return self.attr('src', strip)

    def alt(self, strip=True):
        return self.attr('alt', strip)

    def attr(self, name, strip=True):
        result = self._item.get(name)
        if result is None:
            return ''
        if strip:
            return result.strip()
        return result

    def html(self, pretty=False):
        return lxml.html.tostring(self._item, pretty, encoding='unicode')


class HtmlItems:
    def __init__(self, items=None):
        self._items = []
        items_type = type(items)
        if items_type is None:
            return
        elif items_type == list:
            self.add_items(items)

    def add_items(self, items):
        for item in items:
            item_type = type(item)
            if item_type == HtmlItem:
                self._items.append(item)
            elif item_type == str:
                self._items.append(HtmlItem(item))
            elif item_type == lxml.html.HtmlElement:
                self._items.append(HtmlItem(item))
        return self

    def html(self, strip=True):
        result = []
        for item in self._items:
            result.append(item.Html(strip))
        return result

    def text(self, strip=True):
        result = []
        for item in self._items:
            result.append(item.text(strip))
        return result

    def href(self, strip=True):
        result = []
        for item in self._items:
            result.append(item.href(strip))
        return result

    def src(self, strip=True):
        result = []
        for item in self._items:
            result.append(item.src(strip))
        return result

    def link(self, strip=True):
        result = []
        for item in self._items:
            text = item.text(strip)
            href = item.href(strip)
            result.append({text: href})
        return result

    def img(self, strip=True):
        result = []
        for item in self._items:
            alt = item.alt(strip)
            src = item.src(strip)
            result.append({alt: src})
        return result

    def Attr(self, name, strip=True):
        result = []
        for item in self._items:
            result.append(item.attr(name, strip))
        return result


class HtmlPage(HtmlItem):
    def __init__(self, html, base_url=''):
        super().__init__(html, base_url)
        if base_url != '':
            self._item.make_links_absolute(base_url)
        self.url = base_url


class Str(str):
    def replace_chars(self, chars, to):
        pass
