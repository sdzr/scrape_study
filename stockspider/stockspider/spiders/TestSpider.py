# -*- coding: utf-8 -*-
import scrapy
from stockspider.items import News

class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            new = News()
            new['title']=quote.css("span.text::text").extract_first()
            new['body'] = quote.css("small.author::text").extract_first()
            new['date'] = quote.css("div.tags > a.tag::text").extract()
            yield new
            # yield {
            #     'text': quote.css("span.text::text").extract_first(),
            #     'author': quote.css("small.author::text").extract_first(),
            #     'tags': quote.css("div.tags > a.tag::text").extract()
            # }

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
