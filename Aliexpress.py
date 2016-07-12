from Spider import Spider
from Parser import HtmlPage

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
        html = self.Download(url)
        page = HtmlPage(html)
        # Call function for parse page
        getattr(self, route['name'])(page)
    
    def Category(self, page):
        urls = page.Find('.list-item a.product')
        #self.add_urls(urls, page.Url)
    
    def Item(self, page):
        item = {}
        item['name'] = page.Find('h1.product-name').Text()
        item['price'] = page.Find('#j-sku-price').Text()
        #item['img'] = page.Find('.ui-image-viewer-thumb-frame img').Src()
        #item.category = page.Category 
        self.Save(item, 'Items')
    
    def AllCategory(self, page):
        urls = page.FindAll('.cg-main a').Href()
        self.add_urls(urls, page.url)
        

bot = AliExpress()
bot.Run()