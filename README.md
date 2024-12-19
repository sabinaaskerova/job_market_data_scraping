# Job data webscraping
Data acquisition, extraction and storage project at Université Paris Dauphine-PSL. We created a database of job offers scraped from welcometothejungle.com. Group: Anna Krysta, Nikita Andreev, Sabina Askerova, Caio Rocha.

## Directories

- `data/`: The data downloaded from welcometothejungle.com.
- `jobscraping` Scrapy project.

### **Main Files and Scripts**
- **`wttj_scraping.py`**: Script for initial API scraping.
- **Scrapy Project** (`jobscraping` directory): Contains spiders and logic for scraping company and job information.
  - `spiders/company_list.py`: Scraper for fetching a list of companies.
  - `spiders/company_jobs.py`: Scraper for fetching job details for each company.
- **`parse_json.py`**: Cleans the `companies.json` file for further processing.
- **`company.py`**: Contains the `Company` abstraction class.
- **`analysis.py`**: Analyzes the dataset quality.
- **`db_comp_jobs.py`**: Creates a database file to store job and company data.
- **`data_stats.ipynb`**: Jupyter Notebook for dataset visualization and analysis.




## **Usage**
### 0. Install all dependencies 
`pip install -r requirements.txt`

### 1. Reverse Engineering API from the Main Job Posting Page
To scrape job postings from the main page, execute the following command:
```bash
python wttj_scraping.py
```
This will collect job posting data available on the platform's main page.

---

### 2. Content Exploration

#### a) Install Go
```bash
sudo apt install golang-go
```

#### b) Install Katana
```bash
CGO_ENABLED=1 go install github.com/projectdiscovery/katana/cmd/katana@latest
```
You may need to set the environment variable for Go:
```bash
export PATH=$PATH:/usr/local/go/bin
```

#### c) Explore Links
Run Katana to crawl links with a depth of 3:
```bash
katana -u https://www.welcometothejungle.com/en/companies -d 3 -o companies.txt
```
Filter for alphabetically ordered directories:
```bash
grep "/en/directory/" companies.txt > companies_alphabet.txt
```

**Note**: We could have let Katana fetch all company links, but we opted to scrape them from alphabetically ordered directories for additional exploration with Scrapy.

---

### 3. Start the Scrapy Project

#### a) Create and Initialize Scrapy Project
```bash
scrapy startproject jobscraping
cd jobscraping
```

#### b) Run Company List Scraper
Run the spider to scrape all companies:
```bash
scrapy crawl company_list
```
The resulting company URLs will be saved in `company_urls.txt`.

#### c) Run Job Scraper
Scrape job details for each company:
```bash
scrapy crawl company_jobs
```
Results will be stored in:
- `job_data.json`: Contains job information.
- `company_data.json`: Contains company information.

---

## **Additional Scripts**

### 4. Post-Scraping Data Processing

 Run

- **`python3 parse_json.py`**: Clean and preprocess the `companies.json` file.
- **`python3 analysis.py`**: Analyze the quality of the dataset for insights.
- **`python3 db_comp_jobs.py`**: Create a database file (`db.sqlite3`) to store scraped data. **job_market.db** file will be created under data/.

### 5. Data Visualization
- **`data_stats.ipynb`**: Use this Jupyter Notebook to visualize and analyze the dataset, including company trends and job distribution.

---

<!-- ## **Architecture Explanation**

- **`wttj_scraping.py`**: This script operates independently to interact with the API.
- **Scrapy Project**: 
  - Designed for modular and scalable web scraping.
  - Spiders (`company_list` and `company_jobs`) reside in the `spiders` folder of the Scrapy project (`jobscraping` directory).
- **Support Scripts**:
  - Scripts like `parse_json.py`, `db_comp_jobs.py`, and `analysis.py` work outside the Scrapy project directory for post-scraping processing, analysis, and database management. -->

