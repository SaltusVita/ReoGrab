from Spider import *

class AliExpress(Spider):
    
    def Category(self, page):
        urls = page.find('.list-item a.product').href()
        self.add_urls(urls, page.url)
    
    def Item(self, page):
        item = str()
        item.name = page.find('h1.product-name').text()
        item.price = page.find('#j-sku-price').text()
        item.img = page.find('.ui-image-viewer-thumb-frame img').src()
        item.category = page.category 
        self.Save(item, 'Items')