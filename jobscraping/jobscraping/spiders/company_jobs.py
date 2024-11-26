import scrapy

class CompanySpider(scrapy.Spider):
    name = "company_jobs"
    start_urls = []

    custom_settings = {
        "FEEDS": {
            "company_data.json": {"format": "json", "encoding": "utf8", "indent": 4},
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("companies_alphabet.txt") as f:
            self.start_urls = [line.strip() for line in f if line.strip()]

    def parse(self, response):
        """Parse alphabetic listing pages and follow links to company profiles."""
        # Updated selector to match the provided HTML structure
        company_links = response.css('div[data-testid="directory-results"] div.sc-15yi4tf-1 a::attr(href)').getall()
        for link in company_links:
            yield response.follow(link, callback=self.parse_company)
    
    def parse_company(self, response):
        """Extract company information from individual company pages."""
        company_data = {}

        # Extracting structured information using selectors
        company_data["name"] = response.css(
            '#app > div > div > div > main > header > div.sc-cbPlza.kjvHBB > div > div > h1::text').get()
        company_data["sector"] = response.css(
            '#app > div > div > div > main > header > div.sc-cbPlza.kjvHBB > div > div > div.sc-kufkCr.ihcEQO > div.sc-bXCLTC.bYVHtb > p::text').get()
        company_data["website"] = response.css(
            '#app > div > div > div > main > header > div.sc-cbPlza.kjvHBB > div > div > div.sc-kufkCr.ihcEQO > div:nth-child(3) > p > a::attr(href)').get()
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
