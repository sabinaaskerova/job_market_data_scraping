import scrapy
import json
from urllib.parse import urljoin

class CompanyJobsSpider(scrapy.Spider):
    name = "company_jobs"
    start_urls = []  # Populate with URLs from companies_alphabet.txt
    custom_settings = {
        "FEEDS": {
            "companies.json": {"format": "json", "encoding": "utf8", "indent": 4},
            "jobs.json": {"format": "json", "encoding": "utf8", "indent": 4},
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("companies_alphabet.txt") as f:
            self.start_urls = [line.strip() for line in f if line.strip()]

    def parse(self, response):
        """Parse directory pages to extract company links and names."""
        companies = response.xpath('//div[@data-testid="directory-results"]/div')
        for company in companies:
            company_link = company.xpath('.//a/@href').get()
            company_name = company.xpath('.//h4/text()').get()

            if company_link:
                company_url = urljoin(response.url, company_link)
                yield scrapy.Request(
                    company_url,
                    callback=self.parse_company,
                    meta={"company_name": company_name, "company_url": company_url},
                )

    def parse_company(self, response):
        """Parse company pages and follow to their jobs page."""
        company_name = response.meta["company_name"]
        company_url = response.meta["company_url"]

        # Extract company details
        company_details = {
            "name": company_name,
            "url": company_url,
            "description": response.xpath('//meta[@name="description"]/@content').get(),
        }
        yield {"type": "company", "data": company_details}

        # Follow to the jobs page
        jobs_url = urljoin(company_url, "jobs")
        yield scrapy.Request(
            jobs_url,
            callback=self.parse_jobs,
            meta={"company_name": company_name},
        )

    def parse_jobs(self, response):
        """Parse the jobs page to get job links."""
        company_name = response.meta["company_name"]
        job_links = response.xpath('//a[contains(@href, "/jobs/")]/@href').getall()

        for job_link in job_links:
            job_url = urljoin(response.url, job_link)
            yield scrapy.Request(
                job_url,
                callback=self.parse_job_details,
                meta={"company_name": company_name, "job_url": job_url},
            )

    def parse_job_details(self, response):
        """Parse individual job details."""
        company_name = response.meta["company_name"]
        job_url = response.meta["job_url"]

        job_details = {
            "company": company_name,
            "url": job_url,
            "title": response.xpath('//h1/text()').get(),
            "location": response.xpath('//p[contains(@class, "location")]/text()').get(),
            "description": response.xpath('//div[contains(@class, "job-description")]//text()').getall(),
        }
        yield {"type": "job", "data": job_details}
