# -*- coding: utf-8 -*-
import scrapy
import requests
import re
from lxml import etree
import logging

#
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

class UniqloSpider(scrapy.Spider):
    name = 'uniqlo'
    allowed_domains = ['uniqlo.tmall.com']
    start_urls = ['https://uniqlo.tmall.com/category.htm']

    def parse(self, response):

        url_end = response.xpath("//input[@id='J_ShopAsynSearchURL']/@value").extract_first()
        print(url_end)
        print("-----------------------")
        url_head = requests.utils.urlparse(response.request.url)
        print(url_head)
        url = url_head.scheme + "://" + url_head.netloc + url_end
        yield scrapy.Request(
            url,
            callback=self.parse_produce_list,
        )

    def parse_produce_list(self, response):
        html_str = response.body.decode("gbk")
        html_str = re.sub(r"\\", "", html_str)
        html = etree.HTML(html_str)
        # 八行以后都是热品推荐全部重复，不需要
        dl_list = html.xpath("//div[@class='J_TItems']/div[position()<=8]/dl")
        for dl in dl_list:
            item = {}
            item["item_name"] = dl.xpath(".//dd[@class='detail']/a/text()")[0]
            item["item_href"] = "https:" + dl.xpath(".//dd[@class='detail']/a/@href")[0]
            item["item_price"] = dl.xpath(".//span[@class='c-price']/text()")[0]
            item["sale_num"] = dl.xpath(".//span[@class='sale-num']/text()")[0]
            item["comments_num"] = dl.xpath("./dd[@class='rates']//h4/a/span/text()")
            item["comments_num"] = item["comments_num"][0] if len(item["comments_num"]) > 0 else None
            print(item, "-" * 100)

            # 翻页
        next_url_temp = html.xpath("//a[@class='J_SearchAsync next']/@href")
        print(next_url_temp, "=" * 100)
        next_url = "https:" + next_url_temp[0] if len(next_url_temp) > 0 else None
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse  # 下一页的url地址也是和前面的一样
            )