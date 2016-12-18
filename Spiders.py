'''
Created on 2 сент. 2016 г.

@author: garet
'''

import urllib.request
import queue
import sqlite3
import re
import json
from urllib.parse import urlparse

from Parser import HtmlPage

class BaseSpider:
    
    def __init__(self):
        self.urls = QueueUrls()
        self.cache = SqliteCache('some_db')

    def add_urls(self, urls):
        self.urls.add_urls(urls)

    def add_urls_routed(self, urls):
        result = []
        for url in urls:
            if self.fetch_route(url) is not None:
                result.append(url)
        #print(result)
        self.add_urls(result)

    def add_routes(self, routes):
        pass

    def fetch_route(self, url):
        if not hasattr(self, 'routes'):
            return
        for route in self.routes:
            part_url = re.match(route['re'], url)
            if part_url is not None and part_url.group(0) == url:
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
        #self.clear()

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
            if 'type' in route and hasattr(self, route['type']):
                pass
            if 'name' in route and hasattr(self, route['name']):
                getattr(self, route['name'])(response)
        pass

    def charset(self, headers):
        encode = 'UTF-8'
        if hasattr(headers, 'Content-Type'):
            m = re.search('charset=([a-z 0-9\-\_]+)', self.headers, re.IGNORECASE)
            if m:
                encode = m.group(1)
        return encode

    def get_page(self, url):
        r = self.cache.get(url)
        if r is not None:
            print(r['url'])
            return Response(r)
        r = self.get_data(url)
        self.cache.set(r)
        print('{0} --- {1}'.format(url, r['url']))
        return Response(r)

    @staticmethod
    def get_data(url):
        try:
            r = urllib.request.urlopen(url)
            out = {
                'url': r.geturl(),
                'code': r.getcode(),
                'headers': json.dumps(r.getheaders()),
                'data': r.read()
            }
            return out
        except urllib.error.HTTPError as e:
            out = {
                'url': e.geturl(),
                'code': e.getcode(),
                'headers': json.dumps(e.getheaders()),
                'data': e.read()
            }
            return out


class QueueUrls:

    def __init__(self):
        self._urls_queue = queue.Queue()
        self._urls_set = set()

    def add_url(self, url):
        u = urlparse(url)
        url = u[0] + '://' + u[1] + u[2] + u[3]
        if u[4] != '':
            url += '?' + u[4]
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
            CREATE TABLE IF NOT EXISTS tbl_urls(
                url TEXT primary key not null,
                code INTEGER,
                headers TEXT,
                data BLOB,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );"""
        self._cursor.execute(sql)

    def get(self, url):
        if self._cursor is None:
            self.InitDB()
        sql = "SELECT * FROM tbl_urls WHERE url=?;"
        self._cursor.execute(sql, (url,))
        row = self._cursor.fetchone()
        if row is not None:
            out = {
                'url': row[0],
                'code': row[1],
                'headers': json.loads(row[2]),
                'data': row[3]
            }
            return out
        return None

    def set(self, dat):
        if self._cursor is None:
            self.init_db()
        sql = "INSERT OR REPLACE INTO tbl_urls(url,code,headers,data) VALUES (?,?,?,?);"
        self._cursor.execute(sql, (dat['url'], dat['code'], dat['headers'], dat['data']))
        self._db.commit()


class Download:

    def __init__(self):
        self.method = 'GET'
        self.user_agent = self.random_user_agent()

    @staticmethod
    def random_user_agent(self, browser=None, os=None):
        return 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 8.0; WOW64; Trident/5.0; .NET CLR 2.7.40781; .NET4.0E; en-SG)'

    @staticmethod
    def get_page(url):
        r = urllib.request.urlopen(url)
        code = r.getcode()
        headers = r.getheaders()
        data = r.read()
        url = r.geturl()
        #return Response(r)


class Response:

    def __init__(self, res):
        self.code = res['code']
        self.headers = res['headers']
        self.data = res['data']
        self.url = res['url']

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


