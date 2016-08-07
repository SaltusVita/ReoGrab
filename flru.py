'''
Created on 1 ���. 2016 �.

@author: garet
'''
from Spider import Spider

class FlRu(Spider):
    
    routes = [
                {
                    'name': 'Catalog',
                    're': '[^f]*?fl.ru/freelancers.*?'
                },
                {
                    'name': 'User',
                    're': '[^f]*?fl.ru/users*?'
                },
             ]
    start_urls = ['https://www.fl.ru/freelancers/']
    
    def Catalog(self, page):
        #
        urls = page.FindAll('.b-pager a').Href()
        
        self.AddUrls(urls)
        urls = page.FindAll('.catalog-freelancers a.freelancer-name').Href()
        print(urls)
                
    def User(self, page):
        urls = page.FindAll('a').Href()
        print(urls)

bot = FlRu()
bot.Run()
