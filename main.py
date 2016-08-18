#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et

from MultiSpider import MultiSpider


class FlRu(MultiSpider):
    max_conn = 1
    start_urls = ['https://www.fl.ru/freelancers/']
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

    def Catalog(self, page):
        print(page.status_code)
        print(page.headers)


bot = FlRu()
bot.Run()

