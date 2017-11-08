# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['http://snbook.suning.com/web/trd-fl/999999/0.htm']

    def parse(self, response):
        li_list = response.xpath("//ul[@class='ulwrap']/li")
        for li in li_list:
            item ={}
            item["b_cate"] = li.xpath(".//div[1]/a/text()").extract_first()
            s_list = li.xpath(".//div[2]/a")
            for li in s_list:
                item["s_cate"] = li.xpath("./text()").extract_first()
                item['s_href'] = "http://snbook.suning.com/"+li.xpath("./@href").extract_first()
                yield scrapy.Request(
                    item['s_href'],
                    self.parse_s_list,
                    meta={'item': deepcopy(item)}
                )

    def parse_s_list(self, response):
        item = response.meta['item']
        li_list = response.xpath("//div[@class='filtrate-books list-filtrate-books']/ul/li")
        for li in li_list:
            item["book_img"] = li.xpath("./div[@class='book-img']//img/@src").extract_first()
            item["book_title"] = li.xpath(".//div[@class='book-title']/a/@title").extract_first()
            item["book_publish"] = li.xpath(".//div[@class='book-publish']/a/text()").extract_first()
            item["book_desc"] = li.xpath(".//div[@class='book-descrip c6']/text()").extract_first()
            item["book_href"] = li.xpath("./div[@class='book-img']/a/@href").extract_first()
            yield scrapy.Request(
                item["book_href"],
                callback=self.parse_book_detail,
                meta={'item': deepcopy(item)}
            )
            # 返回下一页 元标签是根据结算动态生成，element下找不到.
            # next_str = li.xpath("/div[@id='pagesbottomxx']/a[@class='next']/@href").extract_first()
            # print(next_str)
            # print("*"*100)
            # num = re.findall(r"turnpage\((\d+)\)", next_str, re.S)[0]
            # if num is not None:
            #     next_url = item['s_href'] + "?pageNumber=" + num + "&sort=0"
            #     print(next_url)
            #     print("="*100)
            #     yield scrapy.Request(next_url, self.parse_s_list, meta={'item': deepcopy(item)})

    def parse_book_detail(self, response):
        item = response.meta['item']
        ret = re.findall(r"\"bp\":'(.*?)',", response.body.decode(), re.S)
        item['price'] = ret
        yield item

