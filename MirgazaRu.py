'''
Created on 15 июл. 2016 г.

@author: garet
'''

from Spider import Spider


class MirazaRu(Spider):
    
    routes =  [
                    {
                        'name': 'Catalog',
                        're': '[^m]*?mirgaza.ru/catalog/.*?'
                    },
                ]
    start_urls = ['http://www.mirgaza.ru/catalog/']
    
    def Catalog(self, page):
        urls = page.Find('a',101).Text()
        print(urls)
        

bot = MirazaRu()
bot.Run()

