import requests
import json
from datetime import datetime

# Define the request URL
url = "https://csekhvms53-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.20.0)%3B%20Browser&search_origin=job_search_client"

# Headers (copied from browser's network tab for this request)
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "7707",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "csekhvms53-dsn.algolia.net",
    "Origin": "https://www.welcometothejungle.com",
    "Referer": "https://www.welcometothejungle.com/",
    "Sec-CH-UA": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Linux"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-algolia-api-key": "4bd8f6215d0cc52b26430765769e65a0",
    "x-algolia-application-id": "CSEKHVMS53"
}

# Function to fetch data for a specific page
def fetch_data(page):
    payload = {
        "requests": [
            {
                "indexName": "wttj_jobs_production_en",
                "params": "attributesToHighlight=name"
                          "&attributesToRetrieve=*"
                          "&clickAnalytics=true"
                          "&hitsPerPage=30"
                          "&maxValuesPerFacet=999"
                          "&analytics=true"
                          "&enableABTest=true"
                          "&userToken=86028995-2a08-43dd-940c-fe39a5713f50"
                          "&analyticsTags=page:jobs_index,language:en"
                          "&facets=benefits,organization.commitments,contract_type,contract_duration_minimum,contract_duration_maximum,has_contract_duration,education_level,has_education_level,experience_level_minimum,has_experience_level_minimum,organization.nb_employees,organization.labels,salary_yearly_minimum,has_salary_yearly_minimum,salary_currency,followedCompanies,language,new_profession.category_reference,new_profession.sub_category_reference,remote,sectors.parent_reference,sectors.reference"
                          "&filters="
                          f"&page={page}"
                          "&query="
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response

# Initialize variables
all_data = []
page = 0
total_hits = 1  # Initialize with a non-zero value to enter the loop

# Loop through pages until all job postings are fetched
while page * 30 < total_hits:
    response = fetch_data(page)
    if response.status_code == 200:
        data = response.json()
        hits = data['results'][0]['hits']
        total_hits = data['results'][0]['nbHits']
        all_data.extend(hits)
        page += 1
        print(f"Fetched page {page}, total hits: {total_hits}")
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
        print("Response:", response.text)
        break

# Save the JSON to a file with a timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"job_postings_{timestamp}.json"
with open(filename, "w", encoding="utf-8") as file:
    json.dump(all_data, file, indent=4, ensure_ascii=False)

print(f"JSON response saved to {filename}")