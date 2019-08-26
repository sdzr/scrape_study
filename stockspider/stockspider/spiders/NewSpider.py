import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from stockspider.items import News

class MySpider(CrawlSpider):
    name = 'caijingwang'
    #allowed_domains = ['caijing.com']
    start_urls = ['http://tech.caijing.com.cn']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(LinkExtractor(allow=('', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('.*caijing.*', )), callback='parse_item',follow=True),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = News()
        item['url'] = response.url
        item['title'] = response.css('div.article h2::text').get()
        item['body'] = ' '.join(response.css('div.article-content p::text').getall())
        item['date'] = response.css('span.news_time::text').get()
        item['author'] = response.css('span.news_name::text').get()
        if item['title'] is not None and '上汽' in item['body'] or '上海汽车' in item['body'] :
            yield item