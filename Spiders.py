'''
Created on 2 сент. 2016 г.

@author: garet
'''

import urllib.request
import queue
import sqlite3
import re


class BaseSpider():
    
    def __init__(self):
        self.urls = QueueUrls()

    def AddUrls(self, urls):
        self.urls.AddUrls(urls)

    def AddRoutes(self, routes):
        pass

    def FetchRoute(self, url):
        if not hasattr(self, 'routes'):
            return
        for route in self.routes:
            if re.match(route['re'], url) != None:
                if 'skip' in route and route['skip'] == True:
                    break
                return route
        return None

    def SaveCache(self, url, data=None):
        pass

    def GetCache(self, url):
        pass

    def Run(self):
        self.Init()
        self.Work()
        self.Clear()

    def Init(self):
        if hasattr(self, 'start_urls'):
            self.AddUrls(self.start_urls)
        if hasattr(self, 'routes'):
            self.AddRoutes(self.routes)

    def Work(self):
        while self.urls.Has():
            url = self.urls.GetUrl()
            route = self.FetchRoute(url)
            if route is not None:
                pass
            response = self.GetPage(url)
            print(response)
        pass

    def Clear(self):
        pass

    def GetPage(self, url):
        request = urllib.request.urlopen(url)
        page = request.read()
        return page.decode('utf-8')


class QueueUrls():

    def __init__(self):
        self._urls_queue = queue.Queue()
        self._urls_set = set()

    def AddUrls(self, urls):
        for url in urls:
            if url not in self._urls_set:
                self._urls_queue.put(url)
                self._urls_set.add(url)
        pass

    def ExistUrl(self, url):
        if url in self._urls_set:
            return True
        return False

    def GetUrl(self):
        return self._urls_queue.get()
    
    def __len__(self):
        return len(self._urls_set)

    def Has(self):
        if len(self) > 0:
            return True
        return False


class SqliteCache():

    def __init__(self, db_name):
        self.db_name = db_name

    def InitDB(self):
        file = self.db_name + '.sqlite'
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

    def Get(self, url):
        if self._cursor == None:
            self.InitDB()
        sql = """SELECT * FROM tbl_urls WHERE url=?;"""
        self._cursor.execute(sql, (url,))
        return self._cursor.fetchone()

    def Set(self, url, data):
        if self._cursor == None:
            self.InitDB()
        sql = """INSERT OR REPLACE INTO tbl_urls(url, html)
        VALUES (?,?);"""
        self._cursor.execute(sql, (url, data) )
        self._db.commit()


class Route:

    def __init__(self):
        pass
    


