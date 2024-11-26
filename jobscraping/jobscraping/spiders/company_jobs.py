import scrapy
from scrapy.item import Item, Field

class CompanyItem(Item):
    name = Field()
    sector = Field()
    website = Field()
    year_of_founding = Field()
    employees = Field()
    gender_breakdown = Field()
    average_age = Field()
    social_links = Field()
    text_blocks = Field()

class JobItem(Item):
    company_name = Field()
    job_title = Field()
    location = Field()
    posted_date = Field()
    contract_type = Field()
    remote_status = Field()
    job_link = Field()

class CompanySpider(scrapy.Spider):
    name = "company_jobs"
    start_urls = []

    custom_settings = {
        "FEEDS": {
            "company_data.json": {
                "format": "json", 
                "encoding": "utf8", 
                "indent": 4,
                "fields_to_export": [
                    "name", "sector", "website", "year_of_founding", 
                    "employees", "gender_breakdown", "average_age", 
                    "social_links", "text_blocks"
                ]
            },
            "job_data.json": {
                "format": "json", 
                "encoding": "utf8", 
                "indent": 4,
                "fields_to_export": [
                    "company_name", "job_title", "location", 
                    "posted_date", "contract_type", "remote_status", 
                    "job_link"
                ]
            }
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("company_urls.txt") as f:
            self.start_urls = [line.strip() for line in f if line.strip()]

    def parse(self, response):
        """Parse links to company profiles."""
        for link in self.start_urls:
            yield response.follow(link, callback=self.parse_company)
    
    def parse_company(self, response):
        """Extract company information from individual company pages."""
        company_item = CompanyItem()

        # Extracting structured information using selectors
        company_item["name"] = response.css('header[data-testid="showcase-header"] h1::text').get()
        company_item["sector"] = response.css('div[data-testid="showcase-header-sector"] p::text').get()
        company_item["website"] = response.css('div[data-testid="showcase-header-website"] a::attr(href)').get()

        company_item["year_of_founding"] = response.css(
            '[data-testid="stats-creation-year"]::text').get()
        company_item["employees"] = response.css(
            '[data-testid="stats-nb-employees"]::text').get()
        company_item["gender_breakdown"] = {
            "women": response.css('[data-testid="stats-parity-women"]::text').get(),
            "men": response.css('[data-testid="stats-parity-men"]::text').get(),
        }
        company_item["average_age"] = response.css(
            '[data-testid="stats-average-age"]::text'
        ).get()

        # Social links
        social_links = {}
        for social in response.css('[data-testid="organization-content-block-social-networks"] a'):
            platform = social.attrib.get("data-testid", "").split("-")[-1]
            link = social.attrib.get("href", "")
            if platform and link:
                social_links[platform] = link
        company_item["social_links"] = social_links

        # Text blocks
        text_blocks = {}
        for block in response.css(
            '[data-testid="organization-content-block-text"]'
        ):
            header = block.css("h4::text").get()
            content = block.css("div.QVIoI p::text, div.QVIoI li::text").getall()
            if header and content:
                text_blocks[header] = " ".join(content)
        company_item["text_blocks"] = text_blocks

        yield company_item
        
        jobs_url = response.url.rstrip("/") + "/jobs"
        yield response.follow(jobs_url, callback=self.parse_job_list, meta={"company_item": company_item})

    def parse_job_list(self, response):
        """Extract job details from the job list page."""
        company_item = response.meta["company_item"]
        company_name = company_item["name"]
        
        # Select all job list items, excluding the spontaneous application item
        job_items = response.css('ul[data-testid="search-results"] > li[data-testid="search-results-list-item-wrapper"]')
        
        for job_item in job_items:
            # Extract job details
            job_details = JobItem()
            job_details["company_name"] = company_name
            job_details["job_title"] = job_item.css('h4 div[role="mark"]::text').get('').strip()
            
            # Find location by selecting the text after the location icon
            job_details["location"] = job_item.xpath(
                './/i[@name="location"]/following-sibling::p//text()'
            ).get('').strip()
            
            job_details["posted_date"] = job_item.css('time::attr(datetime)').get()
            
            # Find contract type by selecting the text after the contract icon
            job_details["contract_type"] = job_item.xpath(
                './/i[@name="contract"]/following-sibling::span/text()'
            ).get('').strip()
            
            # Find remote status by selecting the text after the remote icon
            job_details["remote_status"] = job_item.xpath(
                './/i[@name="remote"]/following-sibling::span/text()'
            ).get('').strip()
            
            job_details["job_link"] = job_item.css('a::attr(href)').get('')
            
            yield job_details