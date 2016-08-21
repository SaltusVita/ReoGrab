#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et

from MultiSpider import MultiSpider


class FlRu(MultiSpider):
    max_conn = 50
    start_urls = ['http://lenta.ru/',]
    routes = [
                {
                    'name': 'Catalog',
                    #'re': '[^f]*?fl.ru/freelancers.*?'
                    're': '.*?'
                },
                {
                    'name': 'User',
                    're': '[^f]*?fl.ru/users*?'
                },
             ]

    def Catalog(self, page):
        print(page.status_code)
        
        urls = page.FindAll('.item img').Src()
        self.AddUrls(urls)


bot = FlRu()
bot.Run()

