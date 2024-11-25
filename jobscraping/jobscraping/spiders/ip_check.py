import scrapy

class IpCheckSpider(scrapy.Spider):
    name = 'ip_check'
    start_urls = ['http://httpbin.org/ip']

    def parse(self, response):
        self.log(response.text)
