from Spider import *

class AliExpress(Spider):
    
    def __init__(self):
        self._routes =  [
            {
                'name': 'Category',
                're': '[^a]+?aliexpress.com/af/category/.+?'
            },
            {
                'name': 'Item',
                're': '[^a]+?aliexpress.com/item/.+?'
            },
            {
                'name': 'AllCategory',
                're': '[^a]+?aliexpress.com/all-wholesale-products.html'
            },
        ]
    
    def Run(self):
        url = 'http://ru.aliexpress.com/af/category/202001195.html'
        route = self.Routing(url)
        getattr(self, route['name'])()
        #page = self.Download(url)
        print(route)
    
    def Category(self, page):
        urls = page.find_all('.list-item a.product').href()
        self.add_urls(urls, page.url)
    
    def Item(self, page):
        item = str()
        item.name = page.find('h1.product-name').text()
        item.price = page.find('#j-sku-price').text()
        item.img = page.find('.ui-image-viewer-thumb-frame img').src()
        item.category = page.category 
        self.Save(item, 'Items')
    
    def AllCategory(self, page):
        urls = page.find_all('.cg-main a').href()
        self.add_urls(urls, page.url)
        

bot = AliExpress()
bot.Run()