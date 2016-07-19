'''
Created on 15 июл. 2016 г.

@author: garet
'''

from Spider import Spider


class MirazaRu(Spider):
    
    routes = [
                {
                    'name': 'Catalog',
                    're': '[^m]*?mirgaza.ru/catalog/.*?'
                },
                {
                    'skip': True,
                    're': '[^m]*?mirgaza.ru/catalog/cart.*?'
                }
             ]
    start_urls = ['http://www.mirgaza.ru/catalog/poletron/fuel-injection-bodies-system-propane/4-cylinder/']
    
    def Catalog(self, page):
        print(page.url)
        urls = page.FindAll('.shop_item a').Href()
        #for url in urls:
        #    print(url)
        self.AddUrls(urls)
        title = page.FindAll('.shop_full_item_tabs h2').Text()
        print(title)
        

bot = MirazaRu()
bot.Run()

