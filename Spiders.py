'''
Created on 2 сент. 2016 г.

@author: garet
'''

import urllib.request
import queue
import sqlite3
import re
from urllib.parse import urlparse

from Parser import HtmlPage

class BaseSpider:
    
    def __init__(self):
        self.urls = QueueUrls()

    def add_urls(self, urls):
        self.urls.add_urls(urls)

    def add_routes(self, routes):
        pass

    def fetch_route(self, url):
        if not hasattr(self, 'routes'):
            return
        for route in self.routes:
            if re.match(route['re'], url) is not None:
                if 'skip' in route and route['skip'] is True:
                    break
                return route
        return None

    def save_cache(self, url, data=None):
        pass

    def get_cache(self, url):
        pass

    def run(self):
        self.init()
        self.work()
        self.clear()

    def init(self):
        if hasattr(self, 'start_urls'):
            self.add_urls(self.start_urls)
        if hasattr(self, 'routes'):
            self.add_routes(self.routes)

    def work(self):
        while not self.urls.empty():
            url = self.urls.get_url()
            response = self.get_page(url)
            route = self.fetch_route(url)
            if route is None:
                continue
            if 'name' in route and hasattr(self, route['name']):
                getattr(self, route['name'])(response)
        pass

    @staticmethod
    def get_page(url):
        r = urllib.request.urlopen(url)
        return Response(r)


class QueueUrls:

    def __init__(self):
        self._urls_queue = queue.Queue()
        self._urls_set = set()

    def add_url(self, url):
        u = urlparse(url)
        url = u[0] + '://' + u[1] + u[2] + u[3]
        if url not in self._urls_set:
            self._urls_queue.put(url)
            self._urls_set.add(url)

    def add_urls(self, urls):
        urls_type = type(urls)
        if urls_type is str:
            self.add_url(urls)
            return
        for url in urls:
            self.add_url(url)

    def exist_url(self, url):
        if url in self._urls_set:
            return True
        return False

    def get_url(self):
        return self._urls_queue.get()

    def empty(self):
        return self._urls_queue.empty()


class SqliteCache:

    def __init__(self, db_name):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
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

    def get(self, url):
        if self._cursor is None:
            self.InitDB()
        sql = "SELECT * FROM tbl_urls WHERE url=?;"
        self._cursor.execute(sql, (url,))
        return self._cursor.fetchone()

    def set(self, url, data):
        if self._cursor is None:
            self.init_db()
        sql = "INSERT OR REPLACE INTO tbl_urls(url,html) VALUES (?,?);"
        self._cursor.execute(sql, (url, data))
        self._db.commit()


class Request:

    def __init__(self):
        self.method = 'GET'
        self.user_agent = self.random_user_agent()

    @staticmethod
    def random_user_agent(self, browser=None, os=None):
        return 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 8.0; WOW64; Trident/5.0; .NET CLR 2.7.40781; .NET4.0E; en-SG)'


class Response:

    def __init__(self, res):
        self._response = res
        self.code = res.getcode()
        self.headers = res.getheaders()
        self.data = res.read()
        self.url = res.geturl()

    def charset(self):
        encode = 'UTF-8'
        if hasattr(self.headers, 'Content-Type'):
            m = re.search('charset=([a-z 0-9\-\_]+)', self.headers, re.IGNORECASE)
            if m:
                encode = m.group(1)
        return encode

    @property
    def html(self):
        encode = self.charset()
        return self.data.decode(encode)

    def parser(self):
        return HtmlPage(self.html, self.url)


