from Spiders import BaseSpider


class FlRu(BaseSpider):

    start_urls = 'https://www.fl.ru/freelancers/#34234'
    routes = [
        #{
        #    'name': 'user',
        #    're': '[^f]*?fl.ru/users/.*?',
        #},
        {
            'name': 'project',
            're': '[^f]*?fl.ru/projects/.*?'
        },
        {
            'name': 'main_page',
            're': '[^f]*?fl.ru.*?',
        },
    ]

    def main_page(self, request):
        p = request.parser()
        print(request.url)
        users = p.FindAll('.freelancer-name').Href()
        self.add_urls(users)


bot = FlRu()
bot.run()
