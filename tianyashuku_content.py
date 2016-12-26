#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-12 19:09:11
# Project: content

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.ty2016.net/cn/lpf2726/106788.html', callback=self.index_page)

   
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('div#header div.nav ul li:gt(0) a').items():
            self.crawl(each.attr.href, callback=self.second_page)
        
              
        
   
    @config(age=10 * 24 * 60 * 60)
    def second_page(self, response):
        num = int(response.doc('div#left div.dede_pages ul.pagelist li span.pageinfo strong:first ').text())
        urls = [response.url+'{}.html'.format(str(i)) for i in range(1,num+1)]
        for each in urls:
            self.crawl(each, callback=self.third_page)
            
            
    @config(age=10 * 24 * 60 * 60)
    def third_page(self, response):
        for each in response.doc('div#left div.leftbox ul li a').items():
            self.crawl(each.attr.href, callback=self.fourth_page)   
            
    @config(age=10 * 24 * 60 * 60)
    def fourth_page(self, response):
        for each in response.doc('div#main div.book dl dd a').items():
            self.crawl(each.attr.href, callback=self.detail_page) 
            

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('div#main h1').text(),
            "content":response.doc('div#main p:eq(1)').text(),
        }
