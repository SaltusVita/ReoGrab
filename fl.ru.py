from Spiders import BaseSpider


class FlRu(BaseSpider):

    #start_urls = 'https://www.fl.ru/users/i3qqq'  #'https://www.fl.ru/freelancers/#34234'
    start_urls = 'https://www.fl.ru/users/i3qqq/'
    routes = [
        {
            'name': 'project',
            're': '[^f]*?fl.ru/users/[^/]*/viewproj.php\?prjid\=.*'
        },
        {
            'name': 'user',
            're': '[^f]*?fl.ru/users/[^/]*/',
        },
        {
            'name': 'category',
            're': '[^f]*?fl.ru/freelancers/.*'
        },
        {
            'name': 'main_page',
            're': '[^f]*?fl.ru/',
        },
    ]

    def main_page(self, request):
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


bot = FlRu()
bot.run()
