#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-12 11:15:00
# Project: tianya_books_names

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.ty2016.net/', callback=self.index_page)
        
        
        
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('div#header div.nav ul li:gt(0) a').items():
            self.crawl(each.attr.href, callback=self.second_page)
        
              
        
   
    @config(age=10 * 24 * 60 * 60)
    def second_page(self, response):
        num = int(response.doc('div#left div.dede_pages ul.pagelist li span.pageinfo strong:first ').text())
        urls = [response.url+'{}.html'.format(str(i)) for i in range(1,num+1)]
        for each in urls:
            self.crawl(each, callback=self.detail_page)
              
            
            

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url":response.url,
           "title": response.doc('div#left div.leftbox ul li a[href]').text(),
        }
