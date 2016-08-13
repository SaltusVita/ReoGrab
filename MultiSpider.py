'''
Created on 7 ���. 2016 �.

@author: garet
'''
import queue
import re
from io import BytesIO

import pycurl
 

class MultiSpider:

    def __init__(self, params=None):
        urls = []
        for i in range(20):
            urls.append('http://lyubertsy.tehnosila.ru/catalog/tehnika_dlya_kuhni/obrabotka_produktov?p={0}'.format(i)) 
        self.max_conn = 10
        self.urls = UrlRoute()
        self.urls.AddUrls(urls)
    
    def Run(self):
        good = 0
        bad = 0
        m = pycurl.CurlMulti()
        m.handles = []
        for i in range(self.max_conn):
            c = self.InitCurl()
            m.handles.append(c)
    
        freelist = m.handles[:]
        num_processed = 0
        while num_processed < self.urls.Counts():
            while not self.urls.Empty() and freelist:
                url = self.urls.Get()
                c = freelist.pop()
                c.url = url
                c.stream = BytesIO()
                c.setopt(pycurl.URL, url)
                c.setopt(pycurl.WRITEFUNCTION, c.stream.write)
                m.add_handle(c)
            while 1:
                ret, num_handles = m.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break
            while 1:
                num_q, ok_list, err_list = m.info_read()
                for c in ok_list:
                    m.remove_handle(c)
                    data = c.stream.getvalue()
                    c.stream = BytesIO()
                    #print('Lenght: {0}'.format(len(data)))
                    print("Success:", c.url, c.getinfo(pycurl.EFFECTIVE_URL))
                    freelist.append(c)
                    good += 1
                for c, errno, errmsg in err_list:
                    m.remove_handle(c)
                    freelist.append(c)
                    print("Failed: ", c.url, errno, errmsg)
                    bad += 1
                num_processed = num_processed + len(ok_list) + len(err_list)
                if num_q == 0:
                    break
            m.select(10.0)
        print(good)
        print(bad)

    def InitCurl(self):
        c = pycurl.Curl()
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.CONNECTTIMEOUT, 30)
        c.setopt(pycurl.TIMEOUT, 300)
        c.setopt(pycurl.NOSIGNAL, 1)
        return c


class UrlRoute:
    
    def __init__(self):
        self._urls = queue.Queue()
        self._urls_set = set()

    def Route(self, url):
        for route in self.routes:
            if re.match(route['re'], url) != None:
                if 'skip' in route and route['skip'] == True:
                    break
                return route
        return None

    def AddUrls(self, urls):
        for url in urls:
            #route = self.Route(url)
            #if route is None:
            #    continue
            #if 'Skip' in route:
            #    continue
            if url not in self._urls_set:
                self._urls.put(url)
                self._urls_set.add(url)
        pass
    
    def Get(self):
        if not self._urls.empty():
            return self._urls.get()
        return None
    
    def Counts(self):
        return self._urls.qsize()

    def Empty(self):
        return self._urls.empty()

spider = MultiSpider()
spider.Run()