from Spider import Spider

class AliExpress(Spider):
    
    cache = 60 * 60 * 24 * 5 # Time cache
    cache_type = 'sqlite'
    
    start_urls = ['http://ru.aliexpress.com/all-wholesale-products.html',]
    routes = [
                {
                    'name': 'Category',
                    're': '[^a]*?aliexpress.com/af/category/.+?|[^a]*?aliexpress.com/category/.+?',
                    'max': 10000
                },
                {
                    'name': 'Item',
                    're': '[^a]*?aliexpress.com/item/.+?',
                    'max': 100000
                },
                {
                    'name': 'AllCategory',
                    're': '[^a]*?aliexpress.com/all-wholesale-products.html'
                },
            ]
    
    def Category(self, page):
        urls = page.Find('#aliGlobalCrumb h1').Text()
        urls = urls.replace('.', '').replace('>', '').replace('\r', '')
        urls = urls.replace('\r', '').replace('\n', '').replace('\t', '').replace('  ', ' ')
        print(urls)
    
    def Item(self, page):
        item = {}
        item['name'] = page.Find('h1.product-name').Text()
        item['price'] = page.Find('#j-sku-price').Text()
        self.Save(item, 'Items')
    
    def AllCategory(self, page):
        urls = page.FindAll('.cg-main a').Href()
        self.AddUrls(urls)
        

bot = AliExpress()
#bot.Run()
