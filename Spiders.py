'''
Created on 2 сент. 2016 г.

@author: garet
'''

import queue
import sqlite3

class BaseSpider():
    
    def __init__(self):
        pass

    def AddUrls(self, urls):
        pass

    def Routing(self, url):
        pass

    def SaveCache(self, url, data=None):
        pass

    def GetCache(self, url):
        pass

    def Run(self):
        pass


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





