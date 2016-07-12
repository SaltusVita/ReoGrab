'''
Created on 7/07/2016

@author: garet
'''

import urllib.request
import queue
import re

class Spider():
    
    def __init__(self):
        pass
    
    def Routing(self, url):
        for route in self._routes:
            if re.match(route['re'], url) != None:
                return route
        return None
    
    def Download(self, url):
        request = urllib.request.urlopen(url)
        page = request.read()
        return page
        return page.decode('utf-8')
    
    def Save(self, item, category):
        pass
        