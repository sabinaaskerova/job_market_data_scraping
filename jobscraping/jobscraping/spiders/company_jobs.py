import scrapy
import logging

class CompanySpider(scrapy.Spider):
    name = "company_jobs"
    start_urls = []

    custom_settings = {
        "FEEDS": {
            "company_data.json": {"format": "json", "encoding": "utf8", "indent": 4},
            "job_data.json": {"format": "json", "encoding": "utf8", "indent": 4},
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("company_urls.txt") as f:
            self.start_urls = [line.strip() for line in f if line.strip()]

    def parse(self, response):
        """Parse links to company profiles."""
        for link in self.start_urls:
            # logging.info(f"Following link: {link}")
            yield response.follow(link, callback=self.parse_company)
    
    def parse_company(self, response):
        """Extract company information from individual company pages."""
        company_data = {}

        # Extracting structured information using selectors
        company_data["name"] = response.css('header[data-testid="showcase-header"] h1::text').get()
        company_data["sector"] = response.css('div[data-testid="showcase-header-sector"] p::text').get()
        company_data["website"] = response.css('div[data-testid="showcase-header-website"] a::attr(href)').get()

        company_data["year_of_founding"] = response.css(
            '[data-testid="stats-creation-year"]::text').get()
        company_data["employees"] = response.css(
            '[data-testid="stats-nb-employees"]::text').get()
        company_data["gender_breakdown"] = {
            "women": response.css('[data-testid="stats-parity-women"]::text').get(),
            "men": response.css('[data-testid="stats-parity-men"]::text').get(),
        }
        company_data["average_age"] = response.css(
            '[data-testid="stats-average-age"]::text'
        ).get()

        # Social links
        social_links = {}
        for social in response.css('[data-testid="organization-content-block-social-networks"] a'):
            platform = social.attrib.get("data-testid", "").split("-")[-1]
            link = social.attrib.get("href", "")
            if platform and link:
                social_links[platform] = link
        company_data["social_links"] = social_links

        # Text blocks
        text_blocks = {}
        for block in response.css(
            '[data-testid="organization-content-block-text"]'
        ):
            header = block.css("h4::text").get()
            content = block.css("div.QVIoI p::text, div.QVIoI li::text").getall()
            if header and content:
                text_blocks[header] = " ".join(content)
        company_data["text_blocks"] = text_blocks

        yield company_data
        
        jobs_url = response.url.rstrip("/") + "/jobs"
        yield response.follow(jobs_url, callback=self.parse_job_list, meta={"company_data": company_data})

    def parse_job_list(self, response):
        """Extract job details from the job list page."""
        company_data = response.meta["company_data"]
        company_name = company_data["name"]
        
        # Select all job list items, excluding the spontaneous application item
        job_items = response.css('ul[data-testid="search-results"] > li[data-testid="search-results-list-item-wrapper"]')
        
        for job_item in job_items:
            # Extract job details
            job_details = {
                'company_name': company_name,
                'job_title': job_item.css('h4 div[role="mark"]::text').get('').strip(),
                
                # Find location by selecting the text after the location icon
                'location': job_item.xpath(
                    './/i[@name="location"]/following-sibling::p//text()'
                ).get('').strip(),
                
                'posted_date': job_item.css('time::attr(datetime)').get(''),
                
                # Find contract type by selecting the text after the contract icon
                'contract_type': job_item.xpath(
                    './/i[@name="contract"]/following-sibling::span/text()'
                ).get('').strip(),
                
                # Find remote status by selecting the text after the remote icon
                'remote_status': job_item.xpath(
                    './/i[@name="remote"]/following-sibling::span/text()'
                ).get('').strip(),
                
                'job_link': job_item.css('a::attr(href)').get('')
            }
            
            yield job_details



