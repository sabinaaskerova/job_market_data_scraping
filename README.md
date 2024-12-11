# Job data webscraping
Data acquisition, extraction and storage project at Université Paris Dauphine-PSL. We created a database of job offers scraped from welcometothejungle.com. Group: Anna Krysta, Nikita Andreev, Sabina Askerova, Caio Rocha.

## Directories

- data/: The data downloaded from welcometothejungle.com.

## Files

- wttj_scraping.py: Script that scrapes the data from welcometothejungle.com.
- parse_json.py: Script that cleans the companies.json file.
- company.py: Module containing the company abstraction.
- analysis.py: Script containing the analysis of the quality of the dataset.
- db_comp_jobs.py: Script that creates the database file.
- data_stats.ipynb: Visualization of the companies dataset.

## Usage

- Install all dependencies with `pip install -r requirements.txt`
- Run `python3 db_comp_jobs.py` and a **job_market.db** file will be created under data/.