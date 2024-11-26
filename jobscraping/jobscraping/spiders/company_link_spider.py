import scrapy
import logging

class CompanyLinkSpider(scrapy.Spider):
    name = "company_list"
    start_urls = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("companies_alphabet.txt") as f:
            self.start_urls = [line.strip() for line in f if line.strip()]

    def parse(self, response):
        """Parse alphabetic listing pages and follow links to company profiles."""
        base_url = "https://www.welcometothejungle.com"
        company_links = response.css('div[data-testid="directory-results"] div.sc-15yi4tf-1 a::attr(href)').getall()
        logging.info(f"Found company links: {company_links}")
        
        with open("company_urls.txt", "a") as f:
            for link in company_links:
                full_url = base_url + link
                f.write(f"{full_url}\n")

