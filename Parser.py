'''
Created on 10 июл. 2016 г.

@author: garet
'''

import lxml.html as html



class HtmlItem():
    
    def __init__(self, item, base_url=''):
        item_type = type(item)
        #if item_type is str:
            #print(item)
        self._item = html.document_fromstring(item)
        #elif item_type is HtmlItem:
        #    self = item # TODO: Переделать!
        
    def Find(self, s:str, number=0):
        type_find = self.TypeFind(s)
        if type_find == 'xpath':
            result = self._item.xpath(s)
        elif type_find == 'css':
            result = self._item.cssselect(s)
        print(type(result[0]))
        print(result)
        return self
        
    def TypeFind(self, s:str):
        return 'css' # TODO: Доделать тест типа поиска
            
            
class HtmlPage(HtmlItem):
    '''
    classdocs
    '''

    def __init__(self, html):
        super().__init__(html)
        
    #def Find(self, attr):
     #   return self
    
    def Text(self, trim=None):
        return ''
    
    def Src(self, trim=True):
        return ''
