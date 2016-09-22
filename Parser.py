'''
Created on 10 июл. 2016 г.

@author: garet
'''

import lxml.html


class HtmlItem():
    
    def __init__(self, item, base_url=''):
        item_type = type(item)
        if item_type is str or item_type is bytes:
            self._item = lxml.html.document_fromstring(item)
        elif item_type is lxml.html.HtmlElement:
            self._item = item
        elif item_type is HtmlItem:
            self = item # TODO: Переделать!
        elif item_type is None:
            self._item = lxml.html.HtmlElement()

    def TypeFind(self, s:str):
        return 'css' # TODO: Доделать проверку типа поиска
    
    def FindItems(self, s:str):
        type_find = self.TypeFind(s)
        result = None
        if type_find == 'xpath':
            result = self._item.xpath(s)
        elif type_find == 'css':
            result = self._item.cssselect(s)
        return result

    def Find(self, s:str, number=0):
        result = self.FindItems(s)
        if result == None:
            return HtmlItem(result)
        if len(result) >= number:
            return HtmlItem(result[number])
        return HtmlItem(result.pop())
    
    def FindAll(self, s:str, start=0, lenght=-1):
        result = self.FindItems(s)
        return HtmlItems(result)
        
    def Text(self, strip=True):
        result = ''.join(self._item.itertext())
        if strip == True:
            return result.strip()
        elif type(strip) == str:
            return result.strip(strip)
        return result
    
    def Href(self, strip=True):
        return self.Attr('href', strip)
    
    def Src(self, strip=True):
        return self.Attr('src', strip)
    
    def Alt(self, strip=True):
        return self.Attr('alt', strip)
    
    def Attr(self, name, strip=True):
        result = self._item.get(name)
        if result == None:
            return ''
        if strip:
            return result.strip()
        return result
    
    def Html(self, pretty=False):
        return lxml.html.tostring(self._item, pretty, encoding='unicode')


class HtmlItems():
    
    def __init__(self, items=None):
        self._items = []
        items_type = type(items)
        if items_type == None:
            return
        elif items_type == list:
            self.AddItems(items)
    
    def AddItems(self, items):
        for item in items:
            item_type = type(item)
            if item_type == HtmlItem:
                self._items.append(item)
            elif item_type == str:
                self._items.append(HtmlItem(item))
            elif item_type == lxml.html.HtmlElement:
                self._items.append(HtmlItem(item))
        return self
    
    def Html(self, strip=True):
        result = []
        for item in self._items:
            result.append(item.Html(strip))
        return result
    
    def Text(self, strip=True):
        result = []
        for item in self._items:
            result.append(item.Text(strip))
        return result
    
    def Href(self, strip=True):
        result = []
        for item in self._items:
            result.append(item.Href(strip))
        return result
    
    def Src(self, strip=True):
        result = []
        for item in self._items:
            result.append(item.Src(strip))
        return result
    
    def Link(self, strip=True):
        result = []
        for item in self._items:
            text = item.Text(strip)
            href = item.Href(strip)
            result.append({text: href})
        return result
    
    def Img(self, strip=True):
        result = []
        for item in self._items:
            alt = item.Alt(strip)
            src = item.Src(strip)
            result.append({alt: src})
        return result
    
    def Attr(self, name, strip=True):
        result = []
        for item in self._items:
            result.append(item.Attr(name, strip))
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

