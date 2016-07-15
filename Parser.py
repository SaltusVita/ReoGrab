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
        elif item_type == None:
            self._item = lxml.html.HtmlElement()

    def TypeFind(self, s:str):
        return 'css' # TODO: Доделать тест типа поиска
    
    def FindItem(self, s:str):
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
        
    def Text(self, strip=True):
        result = ''.join(self._item.itertext())
        if strip:
            return result.strip()
        return result
    
    def Href(self, strip=True):
        return self.Attr('href', strip)
    
    def Src(self, strip=True):
        return self.Attr('src', strip)
    
    def Attr(self, name, strip=True):
        result = self._item.get(name)
        if result == None:
            return ''
        if strip:
            return result.strip()
        return result
    
    def Html(self, pretty=False):
        return lxml.html.tostring(self._item, pretty, encoding='unicode')



class HtmlPage(HtmlItem):

    def __init__(self, html):
        super().__init__(html)
