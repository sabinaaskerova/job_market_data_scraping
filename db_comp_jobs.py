import sqlite3
import json

# we specify the file paths for job offers and companies data
job_offers_json_path = 'data/job_data.json'
companies_json_path = 'data/cleaned_company_data.json'

# we load the job offers data from the JSON file
with open(job_offers_json_path, 'r', encoding='utf-8') as file:
    job_offers = json.load(file)

# we load the companies data from the JSON file
with open(companies_json_path, 'r', encoding='utf-8') as file:
    companies = json.load(file)

# we connect to the SQLite database
connection = sqlite3.connect('data/job_market.db')

# we create a cursor to execute SQL commands
cursor = connection.cursor()

# we create the 'companies' table if it does not already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY,
        name TEXT,
        sector TEXT,
        website TEXT,
        year_of_founding TEXT,
        employees INTEGER,
        gender_breakdown_women INTEGER,
        gender_breakdown_men INTEGER,
        average_age INTEGER,
        social_links_facebook TEXT,
        social_links_linkedin TEXT,
        social_links_twitter TEXT,
        social_links_youtube TEXT,
        presentation TEXT,
        looking_for TEXT,
        good_to_know TEXT,
        language TEXT
    )
''')

# we create the 'jobs' table if it does not already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER,
        job_title TEXT,
        location TEXT,
        posted_date TEXT,
        contract_type TEXT,
        remote_status TEXT,
        job_link TEXT,
        FOREIGN KEY (company_id) REFERENCES companies(id)
    )
''')

# we insert company data into the 'companies' table
for company in companies:
    cursor.execute('''
        INSERT INTO companies (name, sector, website, year_of_founding, employees,
                               gender_breakdown_women, gender_breakdown_men, average_age,
                               social_links_facebook, social_links_linkedin, social_links_twitter, 
                               social_links_youtube, presentation, looking_for, good_to_know, language)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        company['name'], ', '.join(company['sector']), company['website'], company['year_of_founding'], company['employees'],
        company['gender_breakdown']['women'], company['gender_breakdown']['men'], company['average_age'],
        company['social_links'].get('facebook', ''), company['social_links'].get('linkedin', ''), company['social_links'].get('twitter', ''),
        company['social_links'].get('youtube', ''), company['text_blocks'].get('Presentation', ''), 
        company['text_blocks'].get('What they are looking for', ''), company['text_blocks'].get('Good to know', ''), company.get('Language', '')
    ))

# we commit changes to save the company data into the database
connection.commit()

# we insert job offer data into the 'jobs' table
for offer in job_offers:
    company_name = offer['company_name']
    
    # we find the company ID for the current job offer
    cursor.execute('SELECT id FROM companies WHERE name = ?', (company_name,))
    company_id_result = cursor.fetchone()

    # we skip if the company is not found in the database
    if company_id_result is None:
        continue 

    company_id = company_id_result[0]
    job_title = offer['job_title']
    location = offer['location']
    posted_date = offer['posted_date']
    contract_type = offer['contract_type']
    remote_status = offer['remote_status']
    job_link = offer['job_link']
    
    # we insert the job offer into the 'jobs' table
    cursor.execute('''
        INSERT INTO jobs (company_id, job_title, location, posted_date, contract_type, remote_status, job_link)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        company_id, job_title, location, posted_date, contract_type, remote_status, job_link
    ))

# we commit changes to save the job data into the database
connection.commit()

# we close the database connection
connection.close()

print("Database has been saved in the file 'data/job_market.db'.")