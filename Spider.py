'''
Created on 7/07/2016

@author: garet
'''

import urllib.request
import queue
import re
import sqlite3

from Parser import HtmlPage


class Spider():

    def __init__(self):
        self.start_urls = None
        self._urls = queue.Queue()
        self._urls_set = set()

    def Routing(self, url):
        for route in self.routes:
            if re.match(route['re'], url) != None:
                if 'skip' in route and route['skip'] == True:
                    break
                return route
        return None

    def Download(self, url):
        request = urllib.request.urlopen(url)
        page = request.read()
        return page.decode('utf-8')

    def Save(self, item, category):
        print(item)

    def Run(self):
        if self.start_urls != None:
            self.AddUrls(self.start_urls)
        while not self._urls.empty():
            url = self._urls.get()
            route = self.Routing(url)
            html = self.Download(url)
            page = HtmlPage(html, url)
            # Call function for parse page
            getattr(self, route['name'])(page)

    def AddUrls(self, urls):
        for url in urls:
            if self.Routing(url) == None:
                continue
            if url not in self._urls_set:
                self._urls.put(url)
                self._urls_set.add(url)
        pass

    def CachePage(self, url, html):
        pass

class UrlCache:
    
    def __init__(self):
        self._urls = queue.Queue()
        self._urls_set = set()
    
    def Add(self, urls, html='', params=None):
        type_urls = type(urls)
        if type_urls == str:
            self.AddUniq(urls, html, params)
        elif type_urls == list:
            for url in urls:
                self.AddUniq(url, html, params)
        pass
    
    def AddUniq(self, url, html='', params=None):
        if url not in self._urls:
            self._urls.put(url)
            self._urls_set.add(url)
    
    def Get(self, url):
        pass

