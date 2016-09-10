'''
Created on 7/07/2016

@author: garet
'''

import urllib.request
import queue
import re
import sqlite3
import time

from Parser import HtmlPage


class Spider():

    def __init__(self):
        self.InitSqlite()
        self._urls = queue.Queue()
        self._urls_set = set()
        self.stats = False

    def InitSqlite(self):
        file = self.__class__.__name__ + '.sqlite'
        self._db = sqlite3.connect(file)
        self._cursor = self._db.cursor()
        # Create table
        sql = """
            CREATE TABLE IF NOT EXISTS tbl_urls
            ( 
                url text primary key not null, 
                html text, 
                time timestamp DEFAULT CURRENT_TIMESTAMP
            );"""
        self._cursor.execute(sql)

    def CloseDB(self):
        self._cursor.close()

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
            cache = self.FindCache(url)
            if cache == None: 
                html = self.Download(url)
                self.CachePage(url, html)
            else:
                html = cache[1]
            page = HtmlPage(html, url)
            # Call function for parse page
            getattr(self, route['name'])(page)
            if self.stats:
                self.ViewStats()
        pass

    def ViewStats(self):
        print(self._urls.qsize())

    def AddUrls(self, urls):
        for url in urls:
            route = self.Routing(url)
            if route == None:
                continue
            if 'Skip' in route:
                continue
            if url not in self._urls_set:
                self._urls.put(url)
                self._urls_set.add(url)
        pass

    def FindCache(self, url):
        if self._cursor == None:
            return None
        sql = """SELECT * FROM tbl_urls WHERE url=?;"""
        self._cursor.execute(sql, (url,))
        result = self._cursor.fetchone()
        return result

    def CachePage(self, url, html):
        if self._cursor == None:
            return
        sql = """INSERT OR REPLACE INTO tbl_urls(url, html)
        VALUES (?,?);"""
        params = (url, html)
        self._cursor.execute(sql, params)
        self._db.commit()

