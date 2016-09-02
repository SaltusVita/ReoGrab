'''
Created on 2 сент. 2016 г.

@author: garet
'''


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

