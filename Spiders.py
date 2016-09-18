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
        while self.urls.has():
            url = self.urls.get_url()
            route = self.fetch_route(url)
            if route is not None:
                pass
            response = self.get_page(url)
            print(response)
        pass

    def clear(self):
        pass

    def get_page(self, url):
        request = urllib.request.urlopen(url)
        page = request.read()
        return page.decode('utf-8')


class QueueUrls:

    def __init__(self):
        self._urls_queue = queue.Queue()
        self._urls_set = set()

    def add_urls(self, urls):
        for url in urls:
            if url not in self._urls_set:
                self._urls_queue.put(url)
                self._urls_set.add(url)
        pass

    def exist_url(self, url):
        if url in self._urls_set:
            return True
        return False

    def get_url(self):
        return self._urls_queue.get()
    
    def __len__(self):
        return len(self._urls_set)

    def has(self):
        if len(self) > 0:
            return True
        return False


class SqliteCache():

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


