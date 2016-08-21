'''
Created on 07/08/2016

@author: garet
'''
import queue
import re
from io import BytesIO

import pycurl
import chardet
from email.base64mime import body_encode

import Parser

class MultiSpider:

    def __init__(self, params=None):
        if not hasattr(self, 'max_conn'):
            self.max_conn = 1
        if hasattr(self, 'start_urls'):
            self.AddUrls(self.start_urls)
        if hasattr(self, 'routes'):
            self.AddRoutes(self.routes)

    def AddUrls(self, urls):
        if not hasattr(self, 'urls'):
            self.urls = UrlRoute()
        self.urls.AddUrls(urls)

    def AddRoutes(self, routes):
        if not hasattr(self, 'urls'):
            self.urls = UrlRoute()
        self.urls.AddRoutes(routes)

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
        while num_processed < self.urls.Counts():
            while not self.urls.Empty() and freelist:
                c = freelist.pop()
                c.url = self.urls.Get()
                c.setopt(pycurl.URL, c.url)
                m.add_handle(c)
            while 1:
                ret, num_handles = m.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break
            while 1:
                num_q, ok_list, err_list = m.info_read()
                for c in ok_list:
                    m.remove_handle(c)
                    print(c.getinfo(c.EFFECTIVE_URL))
                    self.CallFunction(c)
                    freelist.append(c)
                for c, errno, errmsg in err_list:
                    m.remove_handle(c)
                    freelist.append(c)
                    print("Failed: ", c.url, errno, errmsg)
                num_processed = num_processed + len(ok_list) + len(err_list)
                if num_q == 0:
                    break
            m.select(30.0)

    def CallFunction(self, c):
        print(c.getinfo(pycurl.CONTENT_TYPE))
        # Get headers and body
        data = c.body_io.getvalue()
        headers = c.headers_io.getvalue()
        status_code = c.getinfo(pycurl.HTTP_CODE)
        effective_url = c.getinfo(c.EFFECTIVE_URL)
        # Clear streams from headers and body
        c.body_io = self.TruncateIO(c.body_io)
        c.headers_io = self.TruncateIO(c.headers_io)
        # Call route function for doing work
        route = self.urls.Route(c.url)
        if 'name' in route and hasattr(self, route['name']):
            page = HtmlPage(effective_url, data, headers, status_code)
            getattr(self, route['name'])(page)

    def TruncateIO(self, sio):
        sio.truncate(0)
        sio.seek(0)
        return sio

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
        return len(self._urls_set)

    def Empty(self):
        return self._urls.empty()


class HtmlPage(Parser.HtmlItem):

    def __init__(self, base_url=None, body=None, headers=None, status_code=None):
        body_enc = None
        if headers:
            self.headers = headers.decode()
            m = re.search('charset=([a-z 0-9\-]+)', self.headers, re.IGNORECASE)
            if m:
                body_enc = m.group(1)
        if body:
            if body_enc is None:
                print('chardet')
                body_enc =  chardet.detect(body)['encoding']
            self.body = body.decode(body_enc)
            print(body_enc)
        if status_code:
            self.status_code = status_code
        super().__init__(self.body, base_url)
        if base_url != '':
            self._item.make_links_absolute(base_url)
        self.url = base_url



