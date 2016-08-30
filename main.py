#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et

from MultiSpider import MultiSpider


class FlRu(MultiSpider):
    max_conn = 50
    start_urls = ['http://lenta.ru/',
                  'http://www.esreality.com/post/2740487/re-omg-ctf-server-s/',
                  'https://forums.anandtech.com/threads/omg-hot-quake-4-special-dvd-edition-34-90.1729658/',
                  'http://goodgame.ru/creative/659/']
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
        a = page.html
        pass
        ##urls = page.FindAll('.item a').Src()
        #self.AddUrls(urls)


bot = FlRu()
bot.Run()

