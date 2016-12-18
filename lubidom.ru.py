from Spiders import BaseSpider


class LubidomRu(BaseSpider):

    start_urls = 'https://lubidom.ru/sitemap.xml'
    routes = [
        {
            'name': 'sitemap',
            're': '[^f]*?lubidom.ru/sitemap.xml',
            'type': 'sitemap',
        },
    ]

    def sitemap(self, request):
        p = request.parser()
        links = p.FindAll('a').Href()
        self.add_urls_routed(links)

    def user(self, request):
        p = request.parser()
        links = p.FindAll('a').Href()
        self.add_urls_routed(links)

    def category(self, request):
        p = request.parser()
        links = p.FindAll('a').Href()
        self.add_urls_routed(links)

    def project(self, request):
        p = request.parser()
        links = p.FindAll('a').Href()
        self.add_urls_routed(links)


bot = LubidomRu()
bot.run()
