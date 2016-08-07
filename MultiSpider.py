'''
Created on 7 рту. 2016 у.

@author: garet
'''
import pycurl

class MultiSpider:

    def __init__(self, params):
        pass
    
    def Run(self):
        pass
    
    def InitCurl(self, c):
        c.fp = None
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.CONNECTTIMEOUT, 30)
        c.setopt(pycurl.TIMEOUT, 300)
        c.setopt(pycurl.NOSIGNAL, 1)
        return c