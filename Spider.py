'''
Created on 7/07/2016

@author: garet
'''

import urllib.request
import queue
import re

from Parser import HtmlPage


class Spider():
    
    def __init__(self):
        self._urls = queue()
    
    def Routing(self, url):
        for route in self._routes:
            if re.match(route['re'], url) != None:
                return route
        return None
    
    def Download(self, url):
        request = urllib.request.urlopen(url)
        page = request.read()
        #return page
        return page.decode('utf8')
    
    def Save(self, item, category):
        pass

    def Run(self):
        while not self._urls.Empty:
            url = self._urls.pop()
            route = self.Routing(url)
            html = self.Download(url)
            page = HtmlPage(html)
            # Call function for parse page
            getattr(self, route['name'])(page)

    def AddUrls(self, urls):
        for url in urls:
            self._urls.put(url)

