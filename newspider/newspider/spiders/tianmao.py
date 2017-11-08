# -*- coding: utf-8 -*-
import scrapy
from lxml import etree


class TianmaoSpider(scrapy.Spider):
    name = 'tianmao'
    allowed_domains = ['tmall.com']
    start_urls = ['https://list.tmall.com/search_product.htm?q=%E9%80%9F%E5%86%99&type=p&style=&cat=all&vmarket=']

    def parse(self, response):
        html_str = response.body.decode("gbk")
        print(html_str)
        html = etree.HTML(html_str)

        with open("tmall1.html","w",encoding="gbk") as f:
            f.write(etree.tostring(html).decode("gbk"))
