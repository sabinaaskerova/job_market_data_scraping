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
        print(jobs_url)
        yield response.follow(jobs_url, callback=self.parse_job_list, meta={"company_data": company_data})

    def parse_job_list(self, response):
        """Extract job links from the job list page."""
        company_data = response.meta["company_data"]
        company_name = company_data["name"]
        job_links = response.css('ul[data-testid="search-results"] li a::attr(href)').getall()
  
        # Filter out any unwanted links (like the spontaneous application link)
        job_links = [link for link in job_links if '/jobs/' in link]
        logging.info(f"{company_name} : Found job links: {job_links}")
        for link in job_links:
            yield response.follow(link, callback=self.parse_job, meta={"company_data": company_data})



    def parse_job(self, response):
        """Extract job information from individual job postings."""
        company_data = response.meta['company_data']
        job_data = {}

        # Extract job information using selectors (to be provided)
        job_data["title"] = response.css('#app > div > div > div > div > div.kjbyhm-0.kkMUtC > section > div.sc-bXCLTC.jlqIpd.sc-la-DkbX.eEsAXp.kjbyhm-5.fDBMPS > h2::text').get()
        job_data["location"] = response.css('#app > div > div > div > div > div.kjbyhm-0.kkMUtC > section > div.sc-bXCLTC.jlqIpd.sc-la-DkbX.eEsAXp.kjbyhm-5.fDBMPS > div.sc-bXCLTC.cWuusC > div:nth-child(1) > div.sc-bXCLTC.hdepoj > div:nth-child(2) > span > span::text').get()
            
            # Extract job description from multiple <p> tags
        description_parts = response.css('#the-position-section > div > div.sc-bXCLTC.eCbjRu.sc-1fssv9b-1.fhzEMX > div:nth-child(1) > div > div.sc-1j992t7-0.bWfUsr > div > p::text').getall()
        job_data["description"] = " ".join(description_parts)
            
        additional_description_parts = response.css('#the-position-section > div > div.sc-bXCLTC.eCbjRu.sc-1fssv9b-1.fhzEMX > div:nth-child(3) > div > div.sc-1j992t7-0.bWfUsr > div > p::text, #the-position-section > div > div.sc-bXCLTC.eCbjRu.sc-1fssv9b-1.fhzEMX > div:nth-child(3) > div > div.sc-1j992t7-0.bWfUsr > div > ul > li > p::text').getall()
        job_data["additional_description"] = " ".join(additional_description_parts)
        
        job_data["company_name"] = company_data.get("name", "N/A")
        logging.info(f"Scraped job data: {job_data}")
        yield job_data