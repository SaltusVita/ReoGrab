'''
Created on 3 ���. 2016 �.

@author: garet
'''

from Spider import Spider

class RandewooRu(Spider):
     
    routes = [
                {
                    'name': 'Category',
                    're': '[^r]*?randewoo.ru/category.*?'
                },
                {
                    'name': 'Brand',
                    're': '[^r]*?randewoo.ru/brands.*?',
                    'Skip': True
                },
                {
                    'name': 'Product',
                    're': '[^r]*?randewoo.ru/*?'
                },
             ]
    start_urls = ['http://randewoo.ru/category/parfyumeriya']
    
    def Category(self, page):
        urls = page.FindAll('#pager_cont a').Href()
        self.AddUrls(urls)
        #sidebar_categories
        urls = page.FindAll('#sidebar_categories a').Href()
        self.AddUrls(urls)
        items = page.FindAll('.products__item a').Href()
        self.AddUrls(items)

    def Product(self, page):
        #urls = page.FindAll('a').Href()
        pass

    def Brand(self, page):
        pass
        #urls = page.FindAll('a').Href()
        #print(urls)


bot = RandewooRu()
bot.stats = True
bot.Run()
