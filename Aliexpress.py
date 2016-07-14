from Spider import Spider


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
    
    def Category(self, page):
        urls = page.Find('h1').Html(True)
        print(urls)
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
bot.AddUrls([
                'http://ru.aliexpress.com/af/category/202001195.html',
                'http://ru.aliexpress.com/all-wholesale-products.html',
                'http://ru.aliexpress.com/item/Free-Gift-Flip-case-Gooweel-M13-3G-Smartphone-Android-5-1-mobile-phone-Quad-Core-5/32656980675.html?ws_ab_test=searchweb201556_8,searchweb201602_3_10048_10039_10056_10047_10055_10049_10046_10045_10017_405_404_407_10040,searchweb201603_1&btsid=f4435ae3-0a2a-4318-8cb3-6b6c5844edbf'
             ])
bot.Run()

