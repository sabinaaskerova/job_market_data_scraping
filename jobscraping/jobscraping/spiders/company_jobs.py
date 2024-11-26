import scrapy
from scrapy.exporters import JsonItemExporter

class CompanyItem(scrapy.Item):
    name = scrapy.Field()
    sector = scrapy.Field()
    website = scrapy.Field()
    year_of_founding = scrapy.Field()
    employees = scrapy.Field()
    gender_breakdown = scrapy.Field()
    average_age = scrapy.Field()
    social_links = scrapy.Field()
    text_blocks = scrapy.Field()

class JobItem(scrapy.Item):
    company_name = scrapy.Field()
    job_title = scrapy.Field()
    location = scrapy.Field()
    posted_date = scrapy.Field()
    contract_type = scrapy.Field()
    remote_status = scrapy.Field()
    job_link = scrapy.Field()

class CompanySpider(scrapy.Spider):
    name = "company_jobs"
    start_urls = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Open output files for writing
        self.company_file = open('company_data.json', 'wb')
        self.jobs_file = open('job_data.json', 'wb')
        
        # Create item exporters
        self.company_exporter = JsonItemExporter(self.company_file, ensure_ascii=False, indent=4)
        self.jobs_exporter = JsonItemExporter(self.jobs_file, ensure_ascii=False, indent=4)
        
        # Start the JSON arrays
        self.company_exporter.start_exporting()
        self.jobs_exporter.start_exporting()
        
        # Read company URLs
        with open("company_urls.txt") as f:
            self.start_urls = [line.strip() for line in f if line.strip()]

    def closed(self, reason):
        # Close the exporters and files when spider is done
        self.company_exporter.finish_exporting()
        self.jobs_exporter.finish_exporting()
        self.company_file.close()
        self.jobs_file.close()

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

        # Export company item directly
        self.company_exporter.export_item(company_item)

        jobs_url = response.url.rstrip("/") + "/jobs"
        yield response.follow(jobs_url, callback=self.parse_job_list, meta={"company_name": company_item["name"]})

    def parse_job_list(self, response):
        """Extract job details from the job list page."""
        company_name = response.meta["company_name"]
        
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
            
            # Export job item directly
            self.jobs_exporter.export_item(job_details)