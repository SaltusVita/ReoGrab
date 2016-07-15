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
        urls = page.FindAll('.group_list img').Img()
        print(urls)

bot = MirazaRu()
bot.Run()

