'''
Created on 15 июл. 2016 г.

@author: garet
'''

from Spider import Spider


class MirazaRu(Spider):
    
    routes = [
                {
                    'skip': True,
                    're': '[^m]*?mirgaza.ru/catalog/cart.*?'
                },
                {
                    'name': 'Catalog',
                    're': '[^m]*?mirgaza.ru/catalog/.*?'
                },
             ]
    start_urls = ['http://www.mirgaza.ru/catalog/']
    
    def Catalog(self, page):
        print(page.url)
        urls = page.FindAll('a').Href()
        self.AddUrls(urls)
        title = page.Find('.catalog_group_h1').Text()
        print(title)
        

bot = MirazaRu()
bot.Run()

