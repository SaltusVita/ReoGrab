'''
Created on 07/08/2016

@author: garet
'''
import queue
import re
from io import BytesIO

import pycurl
 

class MultiSpider:

    def __init__(self, params=None):
        """
        urls = []
        for i in range(17613021513, 17613021513 + 100):
            #urls.append('http://ru.aliexpress.com/category/202005148/dresses/{0}.html'.format(i)) 
            #urls.append('http://glasscannon.ru/page/{0}/'.format(i))
            urls.append('http://eu.battle.net/d3/ru/forum/topic/{0}'.format(i))
        self.max_conn = 2
        self.urls = UrlRoute()
        self.urls.AddUrls(urls)
        """
        self.max_conn = 1
        if hasattr(self, 'start_urls'):
            self.AddUrls(self.start_urls)

    def AddUrls(self, urls):
        if not hasattr(self, '_urls'):
            self.urls = UrlRoute()
        self.urls.AddUrls(urls)
    
    def Debug(self, debug_type, debug_msg):
        print("Debug({0}): {1}".format(debug_type, debug_msg))

    def Run(self):
        m = pycurl.CurlMulti()
        m.handles = []
        for i in range(self.max_conn):
            c = self.InitCurl()
            m.handles.append(c)
        freelist = m.handles[:]
        num_processed = 0
        counts_urls = self.urls.Counts()
        while num_processed < counts_urls:
            while not self.urls.Empty() and freelist:
                url = self.urls.Get()
                c = freelist.pop()
                c.url = url
                c.setopt(pycurl.URL, url)
                m.add_handle(c)
            while 1:
                ret, num_handles = m.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break
            while 1:
                num_q, ok_list, err_list = m.info_read()
                for c in ok_list:
                    m.remove_handle(c)
                    data = c.body_io.getvalue()
                    headers = c.headers_io.getvalue()
                    route = self.urls.Route(c.url)
                    print(route)
                    print(c.getinfo(pycurl.INFO_COOKIELIST))
                    #print("Lenght: {0}, Url: {1}".format(len(data), c.url), c.getinfo(pycurl.EFFECTIVE_URL))
                    freelist.append(c)
                for c, errno, errmsg in err_list:
                    m.remove_handle(c)
                    freelist.append(c)
                    print("Failed: ", c.url, errno, errmsg)
                num_processed = num_processed + len(ok_list) + len(err_list)
                if num_q == 0:
                    break
            m.select(30.0)

    def InitCurl(self):
        c = pycurl.Curl()
        c.body_io = BytesIO()
        c.headers_io = BytesIO()
        c.setopt(pycurl.WRITEFUNCTION, c.body_io.write)
        c.setopt(pycurl.HEADERFUNCTION, c.headers_io.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.CONNECTTIMEOUT, 30)
        c.setopt(pycurl.TIMEOUT, 30)
        c.setopt(pycurl.NOSIGNAL, 1)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.TCP_NODELAY, 1)
        #c.setopt(pycurl.DNS_USE_GLOBAL_CACHE, 1)
        c.setopt(pycurl.USERAGENT, self.RandomUserAgent())
        c.setopt(pycurl.ENCODING, 'gzip, deflate')
        c.setopt(pycurl.COOKIEJAR, 'cookies.txt')
        c.setopt(pycurl.COOKIEFILE, 'cookies.txt')
        #c.setopt(pycurl.DEBUGFUNCTION, self.test)
        return c

    def RandomUserAgent(self):
        return 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'


class UrlRoute:
    
    def __init__(self):
        self._urls = queue.Queue()
        self._urls_set = set()
        self._routes = []

    def Route(self, url):
        for route in self._routes:
            if re.match(route['re'], url) != None:
                if 'skip' in route and route['skip'] == True:
                    break
                return route
        return None

    def AddRoutes(self, routes):
        for route in routes:
            self._routes.append(route)

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
        return self._urls._qsize()

    def Empty(self):
        return self._urls.empty()


class Page:
    pass



